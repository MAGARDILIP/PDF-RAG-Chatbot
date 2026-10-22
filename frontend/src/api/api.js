import axios from "axios";

// Base URL of our FastAPI backend
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// Create an axios instance with default settings
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// === Interceptor: Automatically attach auth token to every request ===
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// === Interceptor: Handle 401 Unauthorized globally ===
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Session expired or invalid — clear stored auth and redirect to login
      localStorage.removeItem("auth_token");
      localStorage.removeItem("auth_user");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// === Authentication APIs ===

export async function loginWithGoogle(idToken) {
  const response = await api.post("/auth/google", { id_token: idToken });
  if (response.data.token) {
    localStorage.setItem("auth_token", response.data.token);
    localStorage.setItem("auth_user", JSON.stringify(response.data.user));
  }
  return response.data;
}

export function getStoredUser() {
  try {
    const userStr = localStorage.getItem("auth_user");
    return userStr ? JSON.parse(userStr) : null;
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  return !!localStorage.getItem("auth_token");
}

export function logout() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("auth_user");
  window.location.href = "/login";
}

// === Upload PDF files ===
export async function uploadPDFs(files) {
  const formData = new FormData();
  for (let file of files) {
    formData.append("files", file);
  }
  const response = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

// === Get list of uploaded documents ===
export async function getDocuments() {
  const response = await api.get("/documents");
  return response.data;
}

// === Delete a document ===
export async function deleteDocument(name) {
  const response = await api.delete(`/document/${name}`);
  return response.data;
}

// === Rebuild the vector index ===
export async function rebuildIndex() {
  const response = await api.post("/rebuild-index");
  return response.data;
}

// === Send a chat question ===
export async function sendQuestion(question) {
  const response = await api.post("/chat", { question });
  return response.data;
}

// === Get system stats ===
export async function getStats() {
  const response = await api.get("/stats");
  return response.data;
}

export default api;
