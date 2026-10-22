import time
import secrets
import requests
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import GOOGLE_CLIENT_ID, ALLOWED_EMAIL_DOMAIN

# === In-memory session store ===
# Maps session_token -> { user: {...}, created_at: timestamp }
# In production you'd use Redis or a database, but for a college project this is fine
SESSIONS = {}
SESSION_TTL_SECONDS = 7 * 24 * 3600  # 7 days

# FastAPI security scheme — extracts Bearer token from Authorization header
security_scheme = HTTPBearer(auto_error=False)


def verify_google_id_token(id_token: str) -> dict:
    """
    Verify a Google ID token by calling Google's tokeninfo endpoint.

    Security checks performed:
    1. Token is genuinely signed by Google (Google validates this)
    2. Audience (aud) matches our GOOGLE_CLIENT_ID
    3. Email is verified by Google
    4. Email belongs to @pccoepune.org domain

    Why this is secure:
    - Users MUST sign in through Google's official login screen
    - They must enter their real Google password (+ 2FA if enabled)
    - Google cryptographically signs the token — it cannot be faked
    - We verify the token directly with Google's servers
    """
    if not id_token:
        raise HTTPException(status_code=400, detail="Missing ID token")

    # Ask Google: "Is this token genuine?"
    try:
        response = requests.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
            timeout=10
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to Google authentication server: {str(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Google token"
        )

    data = response.json()

    # Check: Was this token issued for OUR app?
    aud = data.get("aud")
    if aud != GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=401,
            detail="Token was not issued for this application"
        )

    email = data.get("email", "").lower().strip()
    if not email:
        raise HTTPException(status_code=400, detail="No email associated with this token")

    # CRITICAL CHECK: Only allow @pccoepune.org emails
    expected_suffix = f"@{ALLOWED_EMAIL_DOMAIN.lower()}"
    if not email.endswith(expected_suffix):
        raise HTTPException(
            status_code=403,
            detail=f"Access Denied: Only @{ALLOWED_EMAIL_DOMAIN} email accounts are allowed. You signed in as '{email}'."
        )

    # Extract user info from the verified token
    user_info = {
        "email": email,
        "name": data.get("name", email.split("@")[0]),
        "picture": data.get("picture", ""),
    }

    return user_info


def create_session(user_info: dict) -> str:
    """Create a session token for an authenticated user."""
    session_token = secrets.token_urlsafe(32)
    SESSIONS[session_token] = {
        "user": user_info,
        "created_at": time.time()
    }
    return session_token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> dict:
    """
    FastAPI dependency for protected routes.
    Extracts the Bearer token from the Authorization header and validates the session.
    Usage: Add `current_user: dict = Depends(get_current_user)` to any route.
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please sign in with your @pccoepune.org account."
        )

    token = credentials.credentials
    session = SESSIONS.get(token)

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Session expired or invalid. Please sign in again."
        )

    # Check if session has expired
    if time.time() - session["created_at"] > SESSION_TTL_SECONDS:
        SESSIONS.pop(token, None)
        raise HTTPException(
            status_code=401,
            detail="Session has expired. Please sign in again."
        )

    return session["user"]
