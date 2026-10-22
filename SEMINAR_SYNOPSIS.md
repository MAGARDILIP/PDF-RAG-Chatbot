# MCA Seminar Synopsis

**Course:** MCA Semester IV Seminar (MCA24703)  
**Title:** Comparative Study of Transformer Models (BERT vs GPT)  
**Student:** Mr. Dilip Magar (PRN: 125M1H055)  
**Guide:** Dr. Anjana Arakerimath  

---

## 1. Abstract

This seminar presents a comparative study of two widely used Transformer-based language models — BERT (Bidirectional Encoder Representations from Transformers) and GPT (Generative Pre-trained Transformer). Both of these models are built on the Transformer architecture proposed by Vaswani et al. in 2017, but they follow very different design philosophies. BERT uses an encoder-only structure and learns by predicting masked words in a sentence, which makes it good at understanding text meaning. GPT, on the other hand, uses a decoder-only structure and learns by predicting the next word, which makes it suitable for generating text. In this seminar, the internal architecture, training methods, and practical applications of both models are studied and compared across Natural Language Processing (NLP) tasks like text classification, question answering, and text generation. As a practical demonstration, this study also looks at how both model families can work together in a Retrieval-Augmented Generation (RAG) system, where BERT-based models handle document retrieval and reranking, while a GPT-based model generates the final answer. The expected outcome is to develop a clear understanding of which model type is better suited for which kind of NLP task.

*(186 words)*

---

## 2. Introduction

In 2017, Vaswani et al. introduced the Transformer architecture in their paper "Attention Is All You Need," which changed the field of Natural Language Processing completely. Before Transformers, models like RNNs and LSTMs were used for language tasks, but they were slow and struggled with long sentences. The Transformer solved this by using a mechanism called self-attention, which allows the model to look at all words in a sentence at once instead of one by one. After the Transformer was introduced, two major branches emerged. Google released BERT in 2018, which uses only the encoder part and is designed to understand text deeply. OpenAI released GPT in the same year, which uses only the decoder part and is designed to generate text fluently. Today, both models and their successors are used everywhere — from Google Search to ChatGPT. I chose this topic because while working on my mini project (InfoFetch — a PDF chatbot), I used BERT-based models for finding relevant documents and a GPT-based model for generating answers. This made me curious about what exactly makes these two models different and why each one is better at certain tasks.

*(190 words)*

---

## 3. Objectives

- To study and understand the internal architecture of BERT (encoder-only) and GPT (decoder-only) Transformer models.
- To compare their pre-training strategies — Masked Language Modeling (MLM) in BERT versus autoregressive next-word prediction in GPT.
- To evaluate their strengths and weaknesses across different NLP tasks such as text classification, named entity recognition, question answering, and text generation.
- To demonstrate their complementary usage through a practical RAG-based case study (InfoFetch project) where BERT handles retrieval and GPT handles generation.

*(76 words)*

---

## 4. Literature Survey

The Transformer architecture was first proposed by Vaswani et al. (2017) in their landmark paper "Attention Is All You Need." They introduced the self-attention mechanism which allowed models to process all positions in a sequence simultaneously, removing the sequential bottleneck of recurrent networks. This architecture became the foundation for almost all modern NLP models.

Building on this foundation, Devlin et al. (2019) introduced BERT, which uses only the encoder portion of the Transformer. BERT is pre-trained using two tasks: Masked Language Modeling (MLM), where random words in a sentence are hidden and the model learns to predict them, and Next Sentence Prediction (NSP), where the model learns whether two sentences follow each other. Because BERT reads text in both directions (left-to-right and right-to-left simultaneously), it develops a deep understanding of word context. This made BERT very effective for tasks like sentiment analysis, named entity recognition, and extractive question answering.

Around the same time, Radford et al. (2018) at OpenAI introduced GPT, which uses only the decoder portion of the Transformer. Unlike BERT, GPT reads text in one direction (left-to-right) and is trained to predict the next word in a sequence. This autoregressive approach makes GPT naturally good at generating coherent and fluent text. The subsequent versions — GPT-2 (Radford et al., 2019) and GPT-3 (Brown et al., 2020) — scaled the model significantly and demonstrated impressive few-shot and zero-shot learning abilities, meaning the model could perform tasks it was never explicitly trained for.

Reimers and Gurevych (2019) introduced Sentence-BERT, a modification of BERT that produces fixed-size sentence embeddings suitable for efficient semantic similarity comparison. This is particularly useful in information retrieval systems where fast vector comparison is needed across thousands of documents.

Lewis et al. (2020) proposed the Retrieval-Augmented Generation (RAG) framework, which combines retrieval-based methods (typically using BERT-family embeddings) with generation-based methods (typically using GPT-family models). Their work showed that this combination significantly reduces hallucination and improves factual accuracy in knowledge-intensive tasks.

Most existing studies compare BERT and GPT independently on benchmark datasets. However, there is limited work that examines how these two model families can complement each other in a single unified system. This seminar aims to fill that gap by studying both models individually and then demonstrating their combined usage in a practical RAG pipeline.

*(378 words)*

---

## 5. Problem Statement

BERT and GPT are both built on the Transformer architecture, yet they serve fundamentally different purposes — understanding versus generation. Most academic comparisons treat them as competing models, but in real-world applications like chatbots and search engines, they often work together. Students and developers frequently struggle to decide which model to use for a given task. This seminar addresses the need for a clear, practical comparison that highlights when to use BERT, when to use GPT, and how they can complement each other.

*(83 words)*

---

## 6. Plan of Study

The seminar will be carried out in the following phases:

**Phase 1 — Literature Review (Weeks 1–2):** Study the original Transformer paper and the foundational BERT and GPT papers. Understand the self-attention mechanism and how encoder and decoder architectures differ.

**Phase 2 — Architecture Comparison (Weeks 3–4):** Perform a detailed comparison of BERT's encoder-only and GPT's decoder-only architectures. Study their pre-training objectives (MLM vs autoregressive) and fine-tuning approaches.

**Phase 3 — Task-wise Performance Analysis (Weeks 5–7):** Compare both models across NLP tasks — classification, question answering, summarization, and generation — using published benchmarks and research findings.

**Phase 4 — Practical Case Study (Weeks 8–9):** Demonstrate their complementary roles using the InfoFetch RAG project, where Sentence-BERT handles document retrieval and a GPT-based model handles answer generation.

**Phase 5 — Report Writing and Presentation (Weeks 10–12):** Compile all findings into the final seminar report and prepare for the presentation.

*(147 words)*

---

## 7. References

1. A. Vaswani *et al.*, "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, pp. 5998–6008, 2017.
2. J. Devlin, M. W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," in *Proceedings of NAACL-HLT*, pp. 4171–4186, 2019.
3. A. Radford, K. Narasimhan, T. Salimans, and I. Sutskever, "Improving Language Understanding by Generative Pre-Training," *OpenAI Technical Report*, 2018.
4. A. Radford *et al.*, "Language Models are Unsupervised Multitask Learners," *OpenAI Technical Report*, 2019.
5. T. Brown *et al.*, "Language Models are Few-Shot Learners," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 1877–1901, 2020.
6. P. Lewis *et al.*, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 9459–9474, 2020.
7. N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," in *Proceedings of EMNLP*, pp. 3982–3992, 2019.
8. R. Nogueira and K. Cho, "Passage Re-ranking with BERT," *arXiv preprint arXiv:1901.04085*, 2019.
