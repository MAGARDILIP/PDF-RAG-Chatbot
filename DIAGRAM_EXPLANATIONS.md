# Deep Explanation of All Three Diagrams

**Seminar Topic:** Comparative Study of Transformer Models (BERT vs GPT)  
**Student:** Dilip Magar (PRN: 125M1H055)

This document provides a detailed, component-by-component explanation of all three figures used in the seminar report.

---

## Figure 1 — Transformer Architecture (Vaswani et al., 2017)

### Overview

The original Transformer architecture was proposed in the paper *"Attention Is All You Need"* (Vaswani et al., 2017). It is an **encoder-decoder** model designed for sequence-to-sequence tasks like machine translation (e.g., English → Hindi). Unlike RNNs/LSTMs which process words one at a time, the Transformer processes **all words simultaneously** using a mechanism called **self-attention**.

The diagram shows two main halves separated by a dashed line:

| Side | Component | Purpose |
|------|-----------|---------|
| **Left** | Encoder (×N layers) | Reads and understands the input sentence |
| **Right** | Decoder (×N layers) | Generates the output sentence word by word |

---

### Encoder Side (Left) — Component-by-Component

#### 1. Inputs
The raw input sentence (e.g., *"The cat sat on the mat"*) enters at the bottom of the encoder. The sentence is first **tokenized** — split into smaller units (words or subwords) that the model can process.

#### 2. Input Embedding + Positional Encoding
- **Input Embedding:** Each token is converted into a dense numerical vector (typically 512 dimensions). These vectors are learned during training and capture the semantic meaning of each token.
- **Positional Encoding:** Since the Transformer has no concept of word order (unlike RNNs), we add **positional encodings** — fixed or learned vectors that tell the model *where* each word is in the sentence (1st, 2nd, 3rd position, etc.). Vaswani et al. used sine and cosine functions of different frequencies for this.

> **Why both?** The embedding captures *what* the word means; the positional encoding captures *where* it appears. Together, the model knows both meaning and order.

#### 3. Multi-Head Self-Attention
This is the **core innovation** of the Transformer. Self-attention lets every word in the sentence look at every other word to understand context.

**How it works:**
- For each word, three vectors are computed: **Query (Q)**, **Key (K)**, and **Value (V)**.
- The attention score between any two words = dot product of Query of word A with Key of word B, divided by √d_k (scaling factor).
- These scores are passed through **softmax** to get attention weights (probabilities summing to 1).
- The final output for each word = weighted sum of all Value vectors.

**"Multi-Head"** means this process runs in parallel across multiple "heads" (e.g., 8 heads in the original paper). Each head learns to focus on different types of relationships:
- One head might learn grammatical relationships (subject-verb).
- Another might learn semantic relationships (adjective-noun).
- The outputs from all heads are concatenated and linearly projected.

> **Key Insight:** In the encoder, attention is **bidirectional** — every word can attend to every other word in both directions (left and right). This is what makes BERT (encoder-only) so good at understanding.

#### 4. Add & Norm (First Residual Connection)
- **Add (Residual Connection):** The output of the self-attention layer is added to its input (the embedding). This helps prevent the **vanishing gradient problem** in deep networks and allows information to flow directly through the network.
- **Norm (Layer Normalization):** The result is normalized so that values have a mean of 0 and standard deviation of 1. This stabilizes training and helps the model converge faster.

> **Formula:** `LayerNorm(x + SelfAttention(x))`

#### 5. Feed-Forward Network (FFN)
A simple two-layer neural network applied to each position independently:
- First layer: Expands dimensions (512 → 2048) with a ReLU activation.
- Second layer: Projects back (2048 → 512).

This adds non-linearity and allows the model to learn complex transformations that attention alone cannot capture.

> **Formula:** `FFN(x) = max(0, xW₁ + b₁)W₂ + b₂`

#### 6. Add & Norm (Second Residual Connection)
Same as before — adds the FFN output to its input and normalizes.

> **Formula:** `LayerNorm(x + FFN(x))`

#### ×N Layers
This entire block (Self-Attention → Add & Norm → FFN → Add & Norm) is repeated **N times** (N=6 in the original paper). Each layer refines the representation, building progressively deeper understanding of the input.

---

### Decoder Side (Right) — Component-by-Component

#### 1. Outputs (shifted right)
The decoder receives the **previously generated output tokens**, shifted right by one position. During training, this is the target sentence with a start token prepended. The "shifted right" means the decoder at position *i* can only see tokens before position *i* — it cannot cheat by looking at future words.

#### 2. Output Embedding + Positional Encoding
Same concept as the encoder — each output token is converted to an embedding vector, and positional encoding is added.

#### 3. Masked Multi-Head Self-Attention
Similar to encoder self-attention, but with a **mask**: future positions are blocked (set to -∞ before softmax). This ensures the model can only attend to already-generated words.

> **Why mask?** During generation, the model predicts one word at a time. It would be cheating if it could see the word it's supposed to predict.

| Encoder Self-Attention | Decoder Masked Self-Attention |
|------------------------|-------------------------------|
| Can see ALL words (both directions) | Can only see PAST words (left only) |
| Bidirectional | Unidirectional (causal) |

#### 4. Add & Norm (First Residual Connection)
Same as in the encoder.

#### 5. Multi-Head Cross-Attention
This is what **connects the encoder to the decoder**. The diagram shows an arrow labeled "Encoder Output" going from the encoder side to this layer.

**How it works:**
- **Query (Q)** comes from the decoder (what the decoder wants to know).
- **Key (K)** and **Value (V)** come from the encoder output (the understood representation of the input).
- The decoder "asks questions" (queries) about the input, and the encoder "answers" with relevant information.

> **Example:** When translating "The cat sat" to Hindi, and the decoder is generating the Hindi word for "sat," the cross-attention lets it focus on the English word "sat" in the encoder's representation.

#### 6. Add & Norm (Second Residual Connection)
Adds the cross-attention output to its input and normalizes.

#### 7. Feed-Forward Network
Same as in the encoder — a two-layer FFN applied independently to each position.

#### 8. Add & Norm (Third Residual Connection)
Final residual connection and normalization.

#### 9. Linear + Softmax (Output Head)
- **Linear Layer:** Projects the decoder's output vector to a vector of size equal to the vocabulary (e.g., 30,000 words). Each value represents a "score" for that word.
- **Softmax:** Converts these scores into probabilities. The word with the highest probability is selected as the predicted next word.

---

### Data Flow Summary

```
Input Sentence
    ↓
[Input Embedding + Positional Encoding]
    ↓
[Self-Attention → Add&Norm → FFN → Add&Norm] × N
    ↓
Encoder Output ──────────────────────────────────┐
                                                  ↓
Output (shifted right)                    Cross-Attention
    ↓                                         ↓
[Output Embedding + Positional Encoding]     ...
    ↓                                         ↓
[Masked Self-Attn → Add&Norm → Cross-Attn → Add&Norm → FFN → Add&Norm] × N
    ↓
[Linear → Softmax]
    ↓
Predicted Next Word
```

---

### Key Takeaways for Viva

1. The Transformer replaces RNNs/LSTMs with **self-attention** for parallelism and long-range dependency modeling.
2. Encoder uses **bidirectional** attention (sees full sentence); Decoder uses **masked/causal** attention (sees only past words).
3. **Cross-attention** is the bridge — decoder queries the encoder output.
4. **Residual connections** (Add) prevent vanishing gradients; **Layer Norm** stabilizes training.
5. BERT uses only the **encoder** side; GPT uses only the **decoder** side.

---
---

## Figure 2 — BERT vs GPT Architecture Comparison

### Overview

This diagram shows a **side-by-side comparison** of BERT and GPT — two models that both evolved from the Transformer but took opposite halves of it. A vertical dashed line separates the two architectures.

| Aspect | BERT (Left) | GPT (Right) |
|--------|-------------|-------------|
| **Type** | Encoder-Only | Decoder-Only |
| **Introduced** | Google, 2018 | OpenAI, 2018 |
| **Direction** | Bidirectional | Left-to-Right only |
| **Strength** | Understanding text | Generating text |

---

### BERT Side (Left) — Component-by-Component

#### 1. Input: [CLS] + Tokens + [SEP]
BERT's input has a specific format with special tokens:
- **[CLS]** (Classification): Added at the very beginning. The output corresponding to this token is used as the "sentence-level" representation for classification tasks.
- **Tokens**: The actual words/subwords of the input sentence, tokenized using WordPiece tokenizer.
- **[SEP]** (Separator): Marks the end of a sentence. When two sentences are given (e.g., for question-answering), [SEP] separates them.

> **Example Input:** `[CLS] The cat sat on the mat [SEP]`

#### 2. Token + Segment + Position Embeddings
BERT uses **three types** of embeddings added together:
- **Token Embedding:** The semantic meaning of each word/subword (like the Transformer's input embedding).
- **Segment Embedding:** Indicates whether a token belongs to Sentence A or Sentence B. This is needed for tasks like Next Sentence Prediction where two sentences are fed together.
- **Position Embedding:** Encodes the position of each token. Unlike the original Transformer (which uses sine/cosine), BERT uses **learned** positional embeddings.

> **Final input = Token Embedding + Segment Embedding + Position Embedding**

#### 3. Encoder Stack (×12 layers) — Bidirectional Self-Attention
- BERT uses **12 encoder layers** (in BERT-Base; BERT-Large uses 24).
- Each layer applies **Multi-Head Self-Attention** followed by **Add & Norm** and **Feed-Forward Network** (same as the encoder side of the Transformer).
- The double-headed arrow (↔) labeled **"Bidirectional"** indicates that every token can attend to every other token in both directions — left and right simultaneously.

> **Why this matters:** When BERT processes the word "bank" in "I went to the bank to deposit money," it can see both "went" (left context) and "deposit money" (right context) to determine that "bank" means a financial institution, not a riverbank.

#### 4. Output Representations (for each token)
BERT produces a **contextualized embedding vector for every input token**. Unlike static word embeddings (Word2Vec), BERT's output for "bank" is different depending on the surrounding sentence.

- The **[CLS] token's output** is used as a pooled sentence-level representation.
- Individual **token outputs** are used for token-level tasks like NER.

#### 5. Task Output: Classification, NER, QA (fine-tuned)
BERT is fine-tuned for downstream tasks:
- **Text Classification** (sentiment analysis, spam detection): Uses [CLS] output → Linear layer → Softmax.
- **Named Entity Recognition (NER)**: Uses individual token outputs → classify each token as Person/Location/Organization/etc.
- **Question Answering (Extractive)**: Given a passage and a question, predicts the start and end positions of the answer span in the passage.

#### Pre-training: MLM + NSP
BERT is pre-trained with two self-supervised objectives:
- **Masked Language Modeling (MLM):** 15% of input tokens are randomly masked (replaced with [MASK]), and BERT learns to predict the original tokens. This forces bidirectional understanding.
- **Next Sentence Prediction (NSP):** Given two sentences, BERT predicts whether the second sentence actually follows the first in the original text (50% true pairs, 50% random).

---

### GPT Side (Right) — Component-by-Component

#### 1. Input: Token Sequence
GPT's input is simpler — just the raw token sequence without special classification tokens. Tokens are produced using Byte Pair Encoding (BPE) tokenizer.

> **Example Input:** `The cat sat on the mat`

#### 2. Token + Position Embeddings
GPT uses only **two types** of embeddings (no segment embedding, since it processes one sequence at a time):
- **Token Embedding:** Semantic meaning of each token.
- **Position Embedding:** Learned positional embeddings (same as BERT, different from original Transformer).

> **Final input = Token Embedding + Position Embedding**

#### 3. Decoder Stack (×12 layers) — Masked Self-Attention
- GPT uses **12 decoder layers** (in GPT-1; GPT-2 uses 48, GPT-3 uses 96).
- Each layer applies **Masked Multi-Head Self-Attention** (causal attention), where each token can only attend to tokens that came before it.
- The one-way arrow (→) labeled **"Left-to-Right Only"** shows the causal/autoregressive nature.

> **Why this matters:** GPT generates text one token at a time. When predicting the word after "The cat sat on the," it can see all the words up to "the" but NOT any future words. This is exactly how humans write — we don't know the end of the sentence when writing the beginning.

> **Note:** GPT does NOT use cross-attention (no encoder to connect to). It only uses masked self-attention.

#### 4. Output Representations (last token used)
GPT produces contextual embeddings for all tokens, but typically only the **last token's representation** is used for downstream tasks, since it has "seen" all previous tokens.

#### 5. Task Output: Next Token Prediction / Generation
GPT generates text autoregressively:
1. Feed input → Predict next token → Append predicted token → Repeat.
2. For generation tasks, this loop continues until an end-of-sequence token is produced or a maximum length is reached.

GPT can also be fine-tuned for classification by adding a linear head on top of the last token representation, but generation is its primary strength.

#### Pre-training: Autoregressive LM
GPT is pre-trained with a single objective:
- **Next Token Prediction:** Given all previous tokens, predict the next token. The model maximizes the probability P(token_t | token_1, token_2, ..., token_{t-1}).

---

### Head-to-Head Comparison Table

| Feature | BERT | GPT |
|---------|------|-----|
| **Architecture** | Encoder-only | Decoder-only |
| **Attention Direction** | Bidirectional (↔) | Left-to-Right (→) |
| **Special Tokens** | [CLS], [SEP], [MASK] | None (or endoftext) |
| **Embeddings** | Token + Segment + Position | Token + Position |
| **Pre-training Task** | MLM + NSP | Autoregressive LM |
| **Output Used** | All token outputs | Last token output |
| **Strength** | Understanding / Comprehension | Generation / Fluency |
| **Best For** | Classification, NER, QA, Retrieval | Text generation, Chatbots, Summarization |
| **Parameter Count (Base)** | 110M | 117M |
| **Training Data Direction** | Sees future AND past context | Sees only past context |

---

### Key Takeaways for Viva

1. BERT and GPT are both built on the Transformer but use **opposite halves** — encoder vs decoder.
2. BERT's bidirectional attention gives it deeper **understanding**; GPT's causal attention enables **generation**.
3. BERT uses **three embeddings** (token + segment + position); GPT uses **two** (token + position).
4. BERT predicts **masked words**; GPT predicts the **next word** — fundamentally different pre-training strategies.
5. In the InfoFetch RAG project, BERT is used for **retrieval** (understanding queries and documents), while GPT is used for **generation** (producing answers).

---
---

## Figure 3 — RAG Pipeline (BERT + GPT Working Together)

### Overview

This diagram shows the complete **Retrieval-Augmented Generation (RAG)** pipeline — demonstrating how BERT and GPT work **together** in a practical system (the InfoFetch PDF chatbot). The diagram is divided into two phases by a vertical dashed line:

| Phase | Side | Model Used | Purpose |
|-------|------|-----------|---------|
| **Retrieval Phase** | Left | BERT (Sentence-BERT) | Find relevant document chunks |
| **Generation Phase** | Right | GPT (Qwen 3-32B via Groq) | Generate the final answer |

---

### Retrieval Phase (Left Side — BERT) — Component-by-Component

#### 1. PDF Documents Uploaded by User
The starting point of the pipeline. The user uploads one or more PDF files through the chatbot's web interface (built with Streamlit). These PDFs could be research papers, textbooks, manuals, or any text-heavy documents.

#### 2. Text Extraction & Chunking
- **Text Extraction:** The raw text is extracted from each PDF page using a library like PyPDF2 or pdfplumber. Tables, headers, and paragraphs are pulled out as plain text.
- **Chunking:** The extracted text is split into smaller, overlapping segments (chunks) — typically 500–1000 tokens each. Overlapping ensures that important context at chunk boundaries isn't lost.

> **Why chunk?** LLMs have a limited context window. Sending an entire 200-page PDF is impossible. Instead, we send only the most relevant chunks.

#### 3. BERT Embedding (Sentence-BERT)
Each text chunk is passed through a **Sentence-BERT** model (e.g., `all-MiniLM-L6-v2`) to produce a fixed-size **embedding vector** (e.g., 384 dimensions).

**How Sentence-BERT works:**
- Standard BERT produces per-token embeddings, but comparing two sentences requires expensive pairwise computation.
- Sentence-BERT modifies BERT with a **siamese/triplet network** architecture to produce a single embedding per sentence.
- Semantically similar sentences produce vectors that are **close together** in vector space (high cosine similarity).

> **Example:** The chunks "Machine learning is a subset of AI" and "ML falls under artificial intelligence" would produce nearby vectors, even though they use different words.

#### 4. Vector Database (ChromaDB)
The embedding vectors are stored in **ChromaDB** — a lightweight, open-source vector database.

**What ChromaDB does:**
- Stores embedding vectors alongside their original text and metadata (page number, source PDF).
- Supports fast **approximate nearest neighbor (ANN)** search using algorithms like HNSW.
- When given a query vector, it finds the top-K most similar vectors (and their corresponding text chunks) in milliseconds.

The arrow labeled **"Stored vectors"** connects ChromaDB to the query flow below, indicating that these pre-stored vectors are what gets searched.

#### 5. User Asks a Question
The user types a natural language question (e.g., *"What is the attention mechanism?"*) in the chatbot interface. This triggers the retrieval process.

#### 6. Query Embedding (Sentence-BERT)
The user's question is embedded using the **same Sentence-BERT model** used for document chunks. This ensures the query and documents live in the **same vector space** and can be meaningfully compared.

> **Critical:** If different models were used for query and document embedding, the vectors would be in different spaces and cosine similarity would be meaningless.

#### 7. Semantic Search + Cross-Encoder Reranking
This is a **two-stage retrieval** process:

**Stage 1 — Semantic Search (Bi-Encoder):**
- The query embedding is compared against all stored document embeddings using cosine similarity.
- ChromaDB returns the top-K (e.g., top-20) most similar chunks.
- This is **fast** but approximate (bi-encoder independently embeds query and document).

**Stage 2 — Cross-Encoder Reranking:**
- The top-K results are fed into a **cross-encoder** model (e.g., `ms-marco-MiniLM-L-6-v2`).
- Unlike bi-encoders which embed query and document separately, cross-encoders process the **query-document pair together** through BERT, producing a more accurate relevance score.
- The results are re-ranked by this finer score, and the top-3 to top-5 most relevant chunks are selected.

> **Why two stages?** Bi-encoder is fast (can search millions of documents in milliseconds) but less accurate. Cross-encoder is very accurate but slow (can only process ~100 pairs per second). The two-stage approach gives us **both speed and accuracy**.

---

### The Bridge — "Top relevant chunks"

The horizontal arrow labeled **"Top relevant chunks"** crosses the dashed divider from the retrieval side to the generation side. This represents the most critical data handoff in the RAG pipeline — the selected text chunks are sent to the GPT side to be used as context for answer generation.

---

### Generation Phase (Right Side — GPT) — Component-by-Component

#### 8. Prompt Construction + Strict Guardrails
The retrieved chunks are assembled into a **structured prompt** for the GPT model:

```
CONTEXT: [Retrieved chunk 1] [Retrieved chunk 2] [Retrieved chunk 3]
QUESTION: [User's question]
INSTRUCTION: Answer the question ONLY using the provided context.
             If the answer is not found in the context, say so.
```

**Strict Guardrails include:**
- **Context-only instruction:** The model is told to answer ONLY from the provided context, not from its general knowledge. This prevents hallucination.
- **Citation requirement:** The model is asked to cite which chunk/source it used.
- **Scope limitation:** If the question is out of scope, the model should decline rather than make up an answer.

> **Why guardrails?** Without them, GPT might generate plausible-sounding but factually incorrect answers. RAG's whole purpose is to ground generation in real documents.

#### 9. GPT Answer Generation (Groq API — Qwen 3-32B)
The constructed prompt is sent to a **GPT-family model** via the **Groq API** for inference:
- **Qwen 3-32B**: A 32-billion parameter model (decoder-only, GPT-style) used for answer generation.
- **Groq API**: Provides extremely fast inference using custom LPU (Language Processing Unit) hardware, enabling near-instant responses.

The model processes the prompt autoregressively (left-to-right), generating the answer token by token while attending to the provided context through its self-attention mechanism.

#### 10. Answer Found in Context? (Decision Diamond)
After the model generates its response, the system checks whether the answer was actually grounded in the provided context:

- **Yes → Display Answer + Source Citations:** If the model found relevant information in the provided chunks, the answer is displayed to the user along with **source citations** (which PDF, which page, which chunk). This provides transparency and verifiability.

- **No → Out-of-Scope Message:** If the model determines the question cannot be answered from the provided context (e.g., the user asks about quantum physics but uploaded a biology textbook), it returns a polite message like:
  > *"I could not find information about this topic in the uploaded documents. Please try a different question or upload relevant documents."*

> **Why this matters:** This decision point is what makes RAG reliable. Instead of hallucinating an answer (a common problem with standalone GPT), the system honestly says it doesn't know when the documents don't contain the answer.

---

### Complete Data Flow — End to End

```
┌─────────────────────── RETRIEVAL (BERT) ───────────────────────┐
│                                                                 │
│  PDF Upload → Extract Text → Chunk → Sentence-BERT Embed       │
│                                          ↓                      │
│                                     ChromaDB Store              │
│                                          ↓                      │
│  User Question → Sentence-BERT Embed → Semantic Search          │
│                                          ↓                      │
│                                Cross-Encoder Rerank             │
│                                          ↓                      │
│                                  Top Relevant Chunks ───────────┤
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                                                  ↓
┌─────────────────────── GENERATION (GPT) ───────────────────────┐
│                                                                 │
│  Top Chunks + Question → Prompt Construction + Guardrails       │
│                                          ↓                      │
│                              Qwen 3-32B via Groq API            │
│                                          ↓                      │
│                               Answer in Context?                │
│                              ╱                ╲                  │
│                           Yes                  No               │
│                            ↓                    ↓               │
│                 Display Answer +         Out-of-Scope           │
│                 Source Citations          Message                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Why RAG is Better Than Standalone GPT

| Problem with standalone GPT | How RAG solves it |
|------------------------------|-------------------|
| **Hallucination** — generates plausible but false information | Grounds answers in actual documents |
| **Knowledge cutoff** — doesn't know about recent or private data | Uses real-time uploaded documents |
| **No source verification** — no way to check where the answer came from | Provides citations with page numbers |
| **No scope control** — will answer anything, even if it shouldn't | Guardrails limit answers to uploaded content |

---

### Key Takeaways for Viva

1. RAG combines the **understanding power of BERT** (retrieval) with the **generation power of GPT** (answer creation).
2. **Sentence-BERT** converts both documents and queries into the same vector space for meaningful similarity comparison.
3. **Two-stage retrieval** (bi-encoder + cross-encoder) balances speed and accuracy.
4. **Guardrails** in the prompt prevent GPT from hallucinating by forcing it to answer only from the provided context.
5. The **decision diamond** ensures the system honestly declines when it can't find the answer, rather than making one up.
6. This architecture is the same one used in the InfoFetch mini-project, demonstrating the practical application of studying BERT vs GPT.

---
---

## Quick Reference — All Three Figures at a Glance

| Figure | What it Shows | Key Concept | Relevant To |
|--------|---------------|-------------|-------------|
| **Fig 1** — Transformer Architecture | The original encoder-decoder Transformer | Self-attention, cross-attention, positional encoding | Foundation for both BERT and GPT |
| **Fig 2** — BERT vs GPT | Side-by-side comparison of encoder-only vs decoder-only | Bidirectional vs causal attention, MLM vs autoregressive | Core comparison of the seminar topic |
| **Fig 3** — RAG Pipeline | BERT + GPT working together in a real system | Two-stage retrieval, prompt guardrails, hallucination prevention | Practical demonstration (InfoFetch project) |

> **Connection between all three:** Figure 1 is the *foundation* — the original architecture. Figure 2 shows how BERT and GPT each took *one half* of that architecture. Figure 3 shows how *both halves reunite* in a practical RAG system to leverage each model's strengths.
