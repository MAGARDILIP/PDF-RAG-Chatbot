"""
Seminar Report Generator
Generates full seminar report .docx for MCA Semester IV Seminar (MCA24703)
Title: Comparative Study of Transformer Models (BERT vs GPT)
Student: Dilip Magar | PRN: 125M1H055
Guide: Dr. Anjana Arakerimath
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ============================================================
# STUDENT INFO
# ============================================================
TITLE = "Comparative Study of Transformer Models (BERT vs GPT)"
STUDENT_NAME = "Mr. Dilip Magar"
PRN = "125M1H055"
GUIDE_NAME = "Dr. Anjana Arakerimath"
DEPARTMENT = "Department of Master of Computer Application"
TRUST = "Pimpri Chinchwad Education Trust's"
COLLEGE = "Pimpri Chinchwad College of Engineering"
CITY = "Pune - 411044"
ACADEMIC_YEAR = "2026 - 2027"
CERT_DATE = "29th October 2026"
PROGRAM_NAME = "Master of Computer Application (MCA)"
FOOTER_TEXT = "Pimpri Chinchwad College of Engineering \u2013 Department of MCA \u2014 2026-2027"

BASE_DIR = r"d:\Projects_2026\PDF-RAG-Chatbot"
OUTPUT_PATH = os.path.join(BASE_DIR, "Seminar_Report_Dilip_Magar.docx")
FIG1_PATH = os.path.join(BASE_DIR, "fig_transformer_arch.png")
FIG2_PATH = os.path.join(BASE_DIR, "fig_bert_vs_gpt.png")
FIG3_PATH = os.path.join(BASE_DIR, "fig_rag_pipeline.png")


# ============================================================
# CONTENT
# ============================================================

ABSTRACT = (
    "This seminar presents a comparative study of two widely used Transformer-based "
    "language models \u2014 BERT (Bidirectional Encoder Representations from Transformers) "
    "and GPT (Generative Pre-trained Transformer). Both models are built on the "
    "Transformer architecture proposed by Vaswani et al. in 2017, but they follow "
    "very different design philosophies. BERT uses an encoder-only structure and learns "
    "by predicting masked words in a sentence, which makes it good at understanding "
    "text meaning. GPT, on the other hand, uses a decoder-only structure and learns by "
    "predicting the next word, which makes it suitable for generating text. "
    "In this seminar, the internal architecture, training methods, and practical "
    "applications of both models are studied and compared across Natural Language "
    "Processing (NLP) tasks like text classification, question answering, and text "
    "generation. As a practical demonstration, this study also looks at how both model "
    "families can work together in a Retrieval-Augmented Generation (RAG) system, "
    "where BERT-based models handle document retrieval and reranking, while a GPT-based "
    "model generates the final answer. The expected outcome is to develop a clear "
    "understanding of which model type is better suited for which kind of NLP task."
)

KEYWORDS = "Transformer, BERT, GPT, Self-Attention, Natural Language Processing, Retrieval-Augmented Generation, Encoder-Decoder"

ACKNOWLEDGEMENT = (
    "I would like to express my sincere gratitude to my seminar guide, "
    f"{GUIDE_NAME}, for her valuable guidance, constant encouragement, and support "
    "throughout the preparation of this seminar report. Her insights and feedback "
    "helped me understand the topic deeply and present it effectively.\n\n"
    "I am also thankful to the Head of Department and all the faculty members of "
    "the Department of Master of Computer Application, Pimpri Chinchwad College of "
    "Engineering, for providing the necessary resources and a supportive learning "
    "environment.\n\n"
    "I would also like to thank my classmates for their cooperation and useful "
    "discussions during the course of this work.\n\n"
    "Finally, I am grateful to my family for their constant support and motivation."
)

# ---- Chapter 1: Introduction ----
INTRODUCTION = (
    "Natural Language Processing (NLP) is a branch of artificial intelligence that "
    "deals with enabling computers to understand, interpret, and generate human "
    "language. Over the past decade, NLP has evolved from simple rule-based systems "
    "to advanced deep learning models. Before 2017, Recurrent Neural Networks (RNNs) "
    "and LSTMs were dominant, but they processed text sequentially, making them slow "
    "and unable to capture long-range dependencies. In 2017, Vaswani et al. introduced "
    "the Transformer architecture in their paper \"Attention Is All You Need,\" which "
    "replaced sequential processing with a self-attention mechanism that allows the "
    "model to look at all words simultaneously, making models faster and more accurate.\n\n"

    "Following the Transformer's introduction, two major model families emerged. "
    "Google released BERT in 2018, which uses only the Encoder part and is designed "
    "to understand text by reading it in both directions. OpenAI released GPT in the "
    "same year, which uses only the Decoder part and generates text by predicting the "
    "next word. Today, both models power everything from Google Search to ChatGPT. "
    "I chose this topic because while working on my mini project \u2014 the AI-Powered "
    "Document Query System \u2014 I used BERT-based models for retrieval and a GPT-based "
    "model for answer generation, which made me curious about their differences.\n\n"

    "This report is organized as follows: Chapter 2 discusses motivation. Chapter 3 "
    "presents the literature survey. Chapter 4 states the problem statement and "
    "objectives. Chapter 5 provides detailed study of the architectures. Chapter 6 "
    "discusses results and analysis. Chapter 7 concludes with key findings."
)

# ---- Chapter 2: Motivation ----
MOTIVATION = (
    "Transformer-based models have become the backbone of modern AI applications. "
    "The two most discussed model families \u2014 BERT and GPT \u2014 are often presented as "
    "competitors, but this framing is misleading. BERT is an understanding model that "
    "reads text to extract meaning, while GPT is a generation model that produces new "
    "text. Most academic comparisons focus on benchmark scores and mathematical "
    "formulations, which can be difficult for students to follow. There is a need for "
    "a clear, practical comparison that explains differences in simple terms.\n\n"

    "My personal motivation came from building the AI-Powered Document Query System "
    "as a mini project. In that system, I used Sentence-BERT for converting documents "
    "into searchable vectors and a GPT-family model through the Groq API to generate "
    "answers. Seeing both model types work together made me realize they are not "
    "competitors but complementary technologies. This seminar aims to formalize that "
    "understanding through a structured comparative study."
)

# ---- Chapter 3: Literature Survey ----
LITERATURE_SURVEY = (
    "The Transformer architecture was proposed by Vaswani et al. (2017) [1], introducing "
    "self-attention which allows models to process all positions simultaneously, removing "
    "the sequential bottleneck of recurrent networks. This became the foundation for all "
    "modern NLP models.\n\n"

    "Devlin et al. (2019) introduced BERT [2], using only the encoder with bidirectional "
    "training via Masked Language Modeling (MLM) and Next Sentence Prediction (NSP). "
    "BERT-Base has 12 layers (110M parameters) and BERT-Large has 24 layers (340M). "
    "Radford et al. (2018) introduced GPT [3], using only the decoder with autoregressive "
    "training. GPT-2 [4] scaled to 1.5B parameters and GPT-3 [5] to 175B, demonstrating "
    "impressive few-shot learning. Liu et al. (2019) proposed RoBERTa [9], optimizing "
    "BERT's training by removing NSP and using dynamic masking. Raffel et al. (2020) "
    "introduced T5 [10], using the complete encoder-decoder Transformer.\n\n"

    "Reimers and Gurevych (2019) introduced Sentence-BERT [7] for efficient semantic "
    "similarity using Siamese networks. Nogueira and Cho (2019) demonstrated BERT for "
    "passage re-ranking [8] using Cross-Encoders. Lewis et al. (2020) proposed the RAG "
    "framework [6], combining BERT-family retrieval with GPT-family generation, reducing "
    "hallucination and improving factual accuracy.\n\n"

    "Most existing studies compare BERT and GPT independently on benchmarks like GLUE "
    "and SQuAD. This seminar fills the gap by studying both individually and "
    "demonstrating their combined usage in a practical RAG pipeline."
)

# ---- Chapter 4: Problem Statement + Objectives ----
PROBLEM_STATEMENT = (
    "BERT and GPT are both built on the Transformer architecture, yet they serve "
    "fundamentally different purposes \u2014 understanding versus generation. Most academic "
    "comparisons treat them as competing models, evaluating them on the same benchmarks "
    "without acknowledging their complementary nature. In real-world applications like "
    "chatbots, search engines, and document analysis tools, BERT and GPT often work "
    "together \u2014 BERT finds relevant information while GPT generates human-readable "
    "responses. Students and developers frequently struggle to decide which model to "
    "use for a given task, and there is a lack of practical, easy-to-understand "
    "comparisons.\n\n"
    "This seminar addresses the need for a clear, structured comparison that highlights "
    "the architectural differences between BERT and GPT, identifies when to use each "
    "model, and demonstrates how they can complement each other in practical applications."
)

OBJECTIVES = [
    "To study and understand the internal architecture of BERT (encoder-only) and GPT (decoder-only) Transformer models.",
    "To compare their pre-training strategies \u2014 Masked Language Modeling (MLM) in BERT versus autoregressive next-word prediction in GPT.",
    "To evaluate their strengths and weaknesses across different NLP tasks such as text classification, named entity recognition, question answering, and text generation.",
    "To demonstrate their complementary usage through a practical RAG-based case study (AI-Powered Document Query System) where BERT handles retrieval and GPT handles generation.",
]

# ---- Chapter 5: Details of Study ----
SECTION_5_1 = (
    "The Transformer, proposed by Vaswani et al. in 2017, processes all tokens "
    "simultaneously using self-attention, unlike RNNs which process sequentially. "
    "For each token, it computes Query (Q), Key (K), and Value (V) vectors. Attention "
    "scores are calculated via scaled dot-product of Q and K, then applied as weights "
    "to V vectors. Multi-Head Attention runs this computation multiple times in parallel "
    "with different projections, capturing different relationship types.\n\n"

    "As shown in Figure 1, the Transformer has two components. The Encoder reads the "
    "entire input and produces representations using stacked layers of Multi-Head "
    "Self-Attention and Feed-Forward Networks with residual connections. The Decoder "
    "generates output one token at a time using Masked Self-Attention (preventing "
    "attention to future tokens), Cross-Attention (attending to encoder output), and "
    "Feed-Forward Networks. Positional Encoding is added since self-attention has no "
    "inherent notion of token order."
)

SECTION_5_2 = (
    "BERT, introduced by Devlin et al. in 2019, uses only the Encoder portion. Its "
    "key innovation is bidirectional training \u2014 each token attends to every other token "
    "regardless of position. BERT is pre-trained using Masked Language Modeling (MLM), "
    "where 15% of tokens are masked and the model predicts them from both-side context, "
    "and Next Sentence Prediction (NSP), where the model learns whether two sentences "
    "follow each other.\n\n"

    "The input sums Token Embeddings (WordPiece), Segment Embeddings, and Position "
    "Embeddings. A [CLS] token is prepended for classification. After pre-training on "
    "BooksCorpus and Wikipedia (~3.3B words), BERT is fine-tuned by adding a simple "
    "output layer, making it effective for sentiment analysis, NER, extractive QA, "
    "and text classification."
)

SECTION_5_3 = (
    "GPT, introduced by Radford et al. in 2018, uses only the Decoder portion. It is "
    "unidirectional \u2014 each token attends only to previous tokens via masked (causal) "
    "self-attention. GPT is pre-trained using autoregressive language modeling: predicting "
    "the next token at each position, making it excellent at generating coherent text. "
    "The input uses Token Embeddings (Byte Pair Encoding) and learned Position Embeddings.\n\n"

    "The GPT family's most remarkable aspect is scaling. GPT-1 (2018) had 117M parameters, "
    "GPT-2 (2019) scaled to 1.5B with zero-shot capabilities, and GPT-3 (2020) reached "
    "175B parameters, introducing \"in-context learning\" \u2014 performing new tasks from just "
    "a few prompt examples. Figure 2 shows a side-by-side comparison of BERT and GPT."
)

SECTION_5_4 = (
    "Table 1 presents a feature comparison. BERT uses full bidirectional attention while "
    "GPT uses causal attention. This determines their strengths: BERT excels at "
    "understanding tasks (classification, NER, QA) and GPT excels at generation tasks "
    "(text generation, dialogue, code). Their pre-training objectives reinforce these "
    "strengths \u2014 MLM captures deep semantics, autoregressive training produces fluency."
)

SECTION_5_5 = (
    "As a practical demonstration of how BERT and GPT complement each other, this study "
    "references the AI-Powered Document Query System \u2014 a mini project implementing a "
    "Retrieval-Augmented Generation (RAG) pipeline for answering questions from uploaded "
    "PDF documents.\n\n"

    "In this system, BERT-family models handle retrieval. Sentence-BERT "
    "(BAAI/bge-small-en-v1.5) converts document chunks and user queries into vector "
    "embeddings stored in ChromaDB. When a user asks a question, the system finds "
    "semantically similar sections using cosine similarity. A Cross-Encoder "
    "(ms-marco-MiniLM-L-6-v2) then reranks the candidates by reading each query-document "
    "pair through BERT for precise relevance scoring.\n\n"

    "A GPT-family model handles generation. The top-ranked sections are injected into a "
    "prompt with strict guardrails, and the model (Qwen 3-32B via Groq API) generates "
    "answers strictly from the provided context. If no relevant content is found, the "
    "system returns an out-of-scope message instead of hallucinating.\n\n"

    "This RAG pipeline, illustrated in Figure 3, demonstrates that BERT and GPT are "
    "complementary technologies. BERT provides understanding needed to find relevant "
    "information, while GPT provides generative ability to synthesize coherent answers "
    "with source citations."
)

# ---- Table data ----
COMPARISON_TABLE = [
    ["Architecture", "Encoder-only", "Decoder-only"],
    ["Attention Type", "Bidirectional (full)", "Unidirectional (causal)"],
    ["Pre-training Task", "MLM + NSP", "Autoregressive LM"],
    ["Reading Direction", "Both directions", "Left-to-right only"],
    ["Primary Strength", "Text understanding", "Text generation"],
    ["Fine-tuning", "Task-specific output layer", "Prompt-based / fine-tuning"],
    ["Special Tokens", "[CLS], [SEP], [MASK]", "No special tokens"],
    ["Best For", "Classification, NER, QA", "Generation, Dialogue, Code"],
    ["Base Parameters", "110M (BERT-Base)", "117M (GPT-1)"],
    ["Largest Version", "340M (BERT-Large)", "175B (GPT-3)"],
]

TASK_TABLE = [
    ["Text Classification", "BERT", "Bidirectional context captures full meaning"],
    ["Named Entity Recognition", "BERT", "Understands entity context from both sides"],
    ["Extractive QA", "BERT", "Identifies answer spans within given text"],
    ["Sentiment Analysis", "BERT", "Full context understanding of opinion text"],
    ["Text Generation", "GPT", "Autoregressive training produces fluent text"],
    ["Dialogue / Chatbots", "GPT", "Natural conversational text generation"],
    ["Code Generation", "GPT", "Sequential code generation capability"],
    ["Summarization", "Both", "Extractive (BERT) or generative (GPT)"],
    ["Semantic Search", "BERT", "Sentence-BERT embeddings for similarity"],
    ["RAG Systems", "Both", "BERT retrieves, GPT generates"],
]

# ---- Chapter 6: Results Discussion ----
RESULTS_DISCUSSION = (
    "The comparative analysis reveals several key findings, summarized in Table 2. "
    "For understanding tasks (classification, NER, sentiment analysis), BERT consistently "
    "performs better due to bidirectional attention. For generation tasks (creative writing, "
    "dialogue, code), GPT is superior as its autoregressive training directly aligns with "
    "generation. For question answering, extractive QA favors BERT while generative QA "
    "favors GPT.\n\n"

    "The RAG framework demonstrates the optimal combined use pattern. As shown with the "
    "AI-Powered Document Query System, BERT retrieves relevant document sections through "
    "semantic understanding, and GPT synthesizes them into readable answers \u2014 results "
    "neither model achieves alone. Scaling has had different effects: BERT improved through "
    "better training strategies (RoBERTa), while GPT improved through parameter scaling "
    "(117M to 175B), unlocking emergent few-shot learning capabilities."
)

# ---- Chapter 7: Conclusion ----
CONCLUSION = (
    "This seminar presented a comparative study of BERT and GPT. BERT's bidirectional "
    "encoder is superior for understanding tasks (classification, NER, semantic search), "
    "while GPT's unidirectional decoder is superior for generation tasks (text generation, "
    "dialogue, code). The most important finding is that they are complementary \u2014 the RAG "
    "framework demonstrated through the AI-Powered Document Query System shows that "
    "combining BERT for retrieval with GPT for generation produces more accurate results "
    "than either model alone.\n\n"

    "Future directions include exploring encoder-decoder models like T5, investigating "
    "model scaling versus architectural innovation, and studying newer techniques like "
    "mixture-of-experts for improved efficiency."
)

# ---- References (IEEE format) ----
REFERENCES = [
    'A. Vaswani et al., "Attention Is All You Need," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998\u20136008, 2017.',
    'J. Devlin, M. W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," in Proceedings of NAACL-HLT, pp. 4171\u20134186, 2019.',
    'A. Radford, K. Narasimhan, T. Salimans, and I. Sutskever, "Improving Language Understanding by Generative Pre-Training," OpenAI Technical Report, 2018.',
    'A. Radford et al., "Language Models are Unsupervised Multitask Learners," OpenAI Technical Report, 2019.',
    'T. Brown et al., "Language Models are Few-Shot Learners," in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 1877\u20131901, 2020.',
    'P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459\u20139474, 2020.',
    'N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," in Proceedings of EMNLP, pp. 3982\u20133992, 2019.',
    'R. Nogueira and K. Cho, "Passage Re-ranking with BERT," arXiv preprint arXiv:1901.04085, 2019.',
    'Y. Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach," arXiv preprint arXiv:1907.11692, 2019.',
    'C. Raffel et al., "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer," in Journal of Machine Learning Research, vol. 21, pp. 1\u201367, 2020.',
]


# ============================================================
# DIAGRAM GENERATION (Black & White, Self-made)
# ============================================================

def generate_transformer_diagram(path):
    """Fig 1: Simplified Transformer Architecture."""
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    BW, BH = 3.0, 0.7

    def box(x, y, text, w=BW, h=BH, fc='white', fs=8, bold=False):
        r = mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.08", fc=fc, ec='black', lw=1.0)
        ax.add_patch(r)
        ax.text(x, y, text, ha='center', va='center', fontsize=fs,
                fontfamily='serif', fontweight='bold' if bold else 'normal')

    def arr(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.0))

    ax.text(5, 14.5, "Transformer Architecture (Vaswani et al., 2017)",
            ha='center', fontsize=11, fontfamily='serif', fontweight='bold')

    # ENCODER (left)
    EX = 2.8
    enc_rect = mpatches.FancyBboxPatch((0.8, 4.5), 4.0, 8.5,
        boxstyle="round,pad=0.15", fc='#F5F5F5', ec='black', lw=1.2, ls='--')
    ax.add_patch(enc_rect)
    ax.text(EX, 12.6, "ENCODER (\u00d7N layers)", ha='center', fontsize=9,
            fontfamily='serif', fontweight='bold')

    e_steps = [
        ("Input Embedding +\nPositional Encoding", 5.3),
        ("Multi-Head\nSelf-Attention", 6.8),
        ("Add & Norm", 8.1),
        ("Feed-Forward\nNetwork", 9.5),
        ("Add & Norm", 10.8),
    ]
    for txt, y in e_steps:
        box(EX, y, txt)
    for i in range(len(e_steps) - 1):
        arr(EX, e_steps[i][1] + BH / 2, EX, e_steps[i + 1][1] - BH / 2)

    ax.text(EX, 3.5, "Inputs", ha='center', fontsize=9, fontfamily='serif',
            fontweight='bold')
    arr(EX, 3.8, EX, 5.3 - BH / 2)

    # DECODER (right)
    DX = 7.2
    dec_rect = mpatches.FancyBboxPatch((5.2, 2.0), 4.0, 11.0,
        boxstyle="round,pad=0.15", fc='#F5F5F5', ec='black', lw=1.2, ls='--')
    ax.add_patch(dec_rect)
    ax.text(DX, 12.6, "DECODER (\u00d7N layers)", ha='center', fontsize=9,
            fontfamily='serif', fontweight='bold')

    d_steps = [
        ("Output Embedding +\nPositional Encoding", 2.8),
        ("Masked Multi-Head\nSelf-Attention", 4.3),
        ("Add & Norm", 5.6),
        ("Multi-Head\nCross-Attention", 6.8),
        ("Add & Norm", 8.1),
        ("Feed-Forward\nNetwork", 9.5),
        ("Add & Norm", 10.8),
    ]
    for txt, y in d_steps:
        box(DX, y, txt)
    for i in range(len(d_steps) - 1):
        arr(DX, d_steps[i][1] + BH / 2, DX, d_steps[i + 1][1] - BH / 2)

    # Cross-attention arrow
    arr(EX + BW / 2 + 0.05, 10.8, DX - BW / 2 - 0.05, 6.8)
    ax.text(5.0, 9.0, "Encoder\nOutput", ha='center', fontsize=7,
            fontfamily='serif', fontstyle='italic', color='#555')

    # Output on top of decoder
    box(DX, 12.0, "Linear + Softmax", w=2.6, h=0.6, fc='#E8E8E8', fs=7.5, bold=True)
    arr(DX, 10.8 + BH / 2, DX, 12.0 - 0.3)

    ax.text(DX, 1.0, "Outputs (shifted right)", ha='center', fontsize=9,
            fontfamily='serif', fontweight='bold')
    arr(DX, 1.3, DX, 2.8 - BH / 2)

    plt.tight_layout(pad=0.5)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Fig 1 saved: {path}")


def generate_bert_vs_gpt_diagram(path):
    """Fig 2: BERT vs GPT Architecture Comparison."""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    BW, BH = 4.0, 0.7

    def box(x, y, text, w=BW, h=BH, fc='white', fs=8, bold=False):
        r = mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.08", fc=fc, ec='black', lw=1.0)
        ax.add_patch(r)
        ax.text(x, y, text, ha='center', va='center', fontsize=fs,
                fontfamily='serif', fontweight='bold' if bold else 'normal')

    def arr(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.0))

    ax.text(7, 9.7, "BERT vs GPT \u2014 Architecture Comparison",
            ha='center', fontsize=11, fontfamily='serif', fontweight='bold')

    # BERT (Left)
    BX = 3.5
    ax.text(BX, 9.1, "BERT (Encoder-Only)", ha='center', fontsize=10,
            fontfamily='serif', fontweight='bold')
    items_b = [
        ("Input: [CLS] + Tokens + [SEP]", 8.2),
        ("Token + Segment + Position\nEmbeddings", 7.2),
        ("Encoder Stack (\u00d712 layers)\nBidirectional Self-Attention", 5.9),
        ("Output Representations\n(for each token)", 4.6),
        ("Task Output: Classification,\nNER, QA (fine-tuned)", 3.3),
    ]
    for text, y in items_b:
        box(BX, y, text)
    for i in range(len(items_b) - 1):
        arr(BX, items_b[i][1] - BH / 2, BX, items_b[i + 1][1] + BH / 2)

    ax.annotate('', xy=(BX - 1.0, 5.5), xytext=(BX + 1.0, 5.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(BX, 5.15, "Bidirectional", ha='center', fontsize=7,
            fontfamily='serif', fontstyle='italic')
    ax.text(BX, 2.4, "Pre-training: MLM + NSP\nStrength: Understanding",
            ha='center', fontsize=7.5, fontfamily='serif',
            fontstyle='italic', color='#444')

    # GPT (Right)
    GX = 10.5
    ax.text(GX, 9.1, "GPT (Decoder-Only)", ha='center', fontsize=10,
            fontfamily='serif', fontweight='bold')
    items_g = [
        ("Input: Token Sequence", 8.2),
        ("Token + Position\nEmbeddings", 7.2),
        ("Decoder Stack (\u00d712 layers)\nMasked Self-Attention", 5.9),
        ("Output Representations\n(last token used)", 4.6),
        ("Task Output: Next Token\nPrediction / Generation", 3.3),
    ]
    for text, y in items_g:
        box(GX, y, text)
    for i in range(len(items_g) - 1):
        arr(GX, items_g[i][1] - BH / 2, GX, items_g[i + 1][1] + BH / 2)

    ax.annotate('', xy=(GX + 1.0, 5.5), xytext=(GX - 1.0, 5.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(GX, 5.15, "Left-to-Right Only", ha='center', fontsize=7,
            fontfamily='serif', fontstyle='italic')
    ax.text(GX, 2.4, "Pre-training: Autoregressive LM\nStrength: Generation",
            ha='center', fontsize=7.5, fontfamily='serif',
            fontstyle='italic', color='#444')

    ax.plot([7, 7], [2.0, 9.3], 'k--', lw=0.8, alpha=0.4)

    plt.tight_layout(pad=0.5)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Fig 2 saved: {path}")


def generate_rag_pipeline_diagram(path):
    """Fig 3: RAG Pipeline showing BERT + GPT collaboration."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    BW, BH = 3.0, 0.9

    def box(x, y, text, w=BW, h=BH, fc='white', fs=8, bold=False):
        r = mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.08", fc=fc, ec='black', lw=1.0)
        ax.add_patch(r)
        ax.text(x, y, text, ha='center', va='center', fontsize=fs,
                fontfamily='serif', fontweight='bold' if bold else 'normal',
                linespacing=1.3)

    def arr(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.0))

    def lbl(x, y, text, fs=7):
        ax.text(x, y, text, ha='center', va='center', fontsize=fs,
                fontfamily='serif', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.05', fc='white', ec='none'))

    ax.text(7, 12.5, "RAG Pipeline \u2014 BERT + GPT Working Together",
            ha='center', fontsize=11, fontfamily='serif', fontweight='bold')

    ax.text(3.5, 11.7, "\u2014 RETRIEVAL PHASE (BERT) \u2014", ha='center', fontsize=8,
            fontfamily='serif', fontweight='bold', color='#555')
    ax.text(10.5, 11.7, "\u2014 GENERATION PHASE (GPT) \u2014", ha='center', fontsize=8,
            fontfamily='serif', fontweight='bold', color='#555')

    # Left: BERT retrieval
    left = [
        ("PDF Documents\nUploaded by User", 11.0, '#E8E8E8', True),
        ("Text Extraction\n& Chunking", 9.7, 'white', False),
        ("BERT Embedding\n(Sentence-BERT)", 8.4, 'white', False),
        ("Vector Database\n(ChromaDB)", 7.1, 'white', False),
    ]
    for text, y, fc, bold in left:
        box(3.5, y, text, fc=fc, bold=bold)
    for i in range(len(left) - 1):
        arr(3.5, left[i][1] - BH / 2, 3.5, left[i + 1][1] + BH / 2)

    # Query flow
    box(3.5, 5.4, "User Asks\na Question", fc='#E8E8E8', bold=True)
    arr(3.5, 5.4 - BH / 2, 3.5, 4.1 + BH / 2)
    box(3.5, 4.1, "Query Embedding\n(Sentence-BERT)")
    arr(3.5, 4.1 - BH / 2, 3.5, 2.8 + BH / 2)
    box(3.5, 2.8, "Semantic Search +\nCross-Encoder Reranking")

    # ChromaDB to search
    ax.text(4.3, 6.25, "Stored\nvectors", ha='center', fontsize=6.5,
            fontstyle='italic', color='#666', fontfamily='serif')
    arr(3.5, 7.1 - BH / 2, 3.5, 5.4 + BH / 2 + 0.15)

    # Connect to GPT side
    arr(3.5 + BW / 2, 2.8, 10.5 - BW / 2, 2.8)
    lbl(7.0, 3.1, "Top relevant chunks", fs=7)

    # Right: GPT generation
    box(10.5, 2.8, "Prompt Construction\n+ Strict Guardrails")
    arr(10.5, 2.8 + BH / 2, 10.5, 4.3 - BH / 2)
    box(10.5, 4.3, "GPT Answer Generation\n(Groq API \u2014 Qwen 3-32B)")

    # Decision diamond
    dy = 5.8
    dw, dh = 2.8, 1.2
    pts = [(10.5, dy + dh / 2), (10.5 + dw / 2, dy), (10.5, dy - dh / 2), (10.5 - dw / 2, dy)]
    ax.add_patch(plt.Polygon(pts, fc='#EDEDED', ec='black', lw=1.0))
    ax.text(10.5, dy, "Answer Found\nin Context?", ha='center', va='center',
            fontsize=7.5, fontfamily='serif')
    arr(10.5, 4.3 + BH / 2, 10.5, dy - dh / 2)

    # Yes path
    arr(10.5, dy + dh / 2, 10.5, 7.5 - BH / 2)
    lbl(10.8, dy + dh / 2 + 0.25, "Yes", fs=7)
    box(10.5, 7.5, "Display Answer +\nSource Citations", fc='#E8E8E8', bold=True)

    # No path
    arr(10.5 + dw / 2, dy, 13.0, dy)
    box(13.0, dy, "Out-of-Scope\nMessage", w=2.0, h=0.8, fc='#E0E0E0', fs=7.5, bold=True)
    lbl(10.5 + dw / 2 + 0.5, dy + 0.25, "No", fs=7)

    ax.plot([7, 7], [1.5, 12.0], 'k--', lw=0.8, alpha=0.3)

    plt.tight_layout(pad=0.5)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Fig 3 saved: {path}")


# ============================================================
# DOCUMENT HELPERS
# ============================================================

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
    """Set font properties on a run."""
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_footer(doc):
    """Add footer to all sections."""
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(FOOTER_TEXT)
        set_font(run, size=10)


def add_chapter_title(doc, text):
    """Chapter title: 14pt, BOLD, ALL CAPS, CENTER."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text.upper())
    set_font(run, size=14, bold=True)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)


def add_section_heading(doc, text):
    """Section heading: 12pt, Bold, Capitalized, Left."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_font(run, size=12, bold=True)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)


def add_body(doc, text):
    """Body paragraph: 12pt, justified, 1.5 spacing, 5-space indent."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_font(run, size=12)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.space_after = Pt(12)


def add_body_multi(doc, text):
    """Add multiple paragraphs split by \\n\\n."""
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            add_body(doc, para)


def add_bullet(doc, text):
    """Bullet point with 1.5 line spacing."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.clear()
    run = p.add_run(text)
    set_font(run, size=12)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(4)


def add_figure(doc, image_path, caption, fig_num):
    """Insert figure with caption below (10pt)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=Inches(4.2))
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"Figure {fig_num}: {caption}")
    set_font(run, size=10, bold=True)
    p.paragraph_format.space_after = Pt(12)


def add_table_with_data(doc, headers, data, caption, table_num):
    """Insert table with caption on top (10pt)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"Table {table_num}: {caption}")
    set_font(run, size=10, bold=True)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'

    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for paragraph in hdr[i].paragraphs:
            for run in paragraph.runs:
                set_font(run, size=10, bold=True)

    for row_data in data:
        cells = table.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = val
            for paragraph in cells[i].paragraphs:
                for run in paragraph.runs:
                    set_font(run, size=10)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)


def add_blank(doc, count=1):
    """Add empty paragraphs."""
    for _ in range(count):
        p = doc.add_paragraph()
        run = p.add_run()
        set_font(run, size=12)


# ============================================================
# DOCUMENT ASSEMBLY
# ============================================================

def create_report():
    """Generate the complete seminar report."""
    print("Generating diagrams...")
    generate_transformer_diagram(FIG1_PATH)
    generate_bert_vs_gpt_diagram(FIG2_PATH)
    generate_rag_pipeline_diagram(FIG3_PATH)

    doc = Document()

    # Default style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Page margins
    for section in doc.sections:
        section.top_margin = Mm(25.4)
        section.bottom_margin = Mm(37)
        section.left_margin = Mm(25.4)
        section.right_margin = Mm(32)

    add_footer(doc)

    # ==== COVER PAGE ====
    add_blank(doc, 1)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Seminar Report")
    set_font(run, size=16, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("On")
    set_font(run, size=12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'"{TITLE}"')
    set_font(run, size=18, bold=True)

    add_blank(doc, 1)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Submitted By")
    set_font(run, size=12, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"{STUDENT_NAME}  (PRN: {PRN})")
    set_font(run, size=12)

    add_blank(doc, 1)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Under the Guidance of")
    set_font(run, size=12, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(GUIDE_NAME)
    set_font(run, size=12)

    add_blank(doc, 2)

    for text, bold in [(DEPARTMENT, True), (TRUST, False), (COLLEGE, True), (CITY, False)]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        set_font(run, size=12, bold=bold)

    doc.add_page_break()

    # ==== CERTIFICATE ====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("CERTIFICATE")
    set_font(run, size=14, bold=True)
    p.paragraph_format.space_before = Pt(24)

    cert_text = (
        f'This is to certify that the seminar report entitled "{TITLE}" '
        f'being submitted by {STUDENT_NAME.replace("Mr. ", "")} (PRN: {PRN}) '
        f'is a record of bonafide work carried out by him under the supervision '
        f'and guidance of {GUIDE_NAME} in partial fulfillment of the requirement '
        f'for {PROGRAM_NAME} course of Savitribai Phule Pune University, Pune '
        f'in the academic year {ACADEMIC_YEAR}.'
    )
    add_body(doc, cert_text)

    add_blank(doc, 1)

    p = doc.add_paragraph()
    run = p.add_run(f"Date: {CERT_DATE}")
    set_font(run, size=12)

    p = doc.add_paragraph()
    run = p.add_run("Place: Pune")
    set_font(run, size=12)

    add_blank(doc, 3)

    p = doc.add_paragraph()
    run = p.add_run(GUIDE_NAME)
    set_font(run, size=12)
    p = doc.add_paragraph()
    run = p.add_run("(Seminar Guide)")
    set_font(run, size=12, italic=True)

    add_blank(doc, 1)

    p = doc.add_paragraph()
    run = p.add_run("Head of the Department")
    set_font(run, size=12)

    doc.add_page_break()

    # ==== ABSTRACT & KEYWORDS ====
    add_chapter_title(doc, "Abstract")
    add_body(doc, ABSTRACT)
    p = doc.add_paragraph()
    run = p.add_run(f"Keywords: {KEYWORDS}")
    set_font(run, size=12, bold=True)
    p.paragraph_format.space_before = Pt(12)

    # ==== ACKNOWLEDGEMENT (same page as abstract) ====
    add_chapter_title(doc, "Acknowledgement")
    add_body_multi(doc, ACKNOWLEDGEMENT)

    doc.add_page_break()

    # ==== TABLE OF CONTENTS ====
    add_chapter_title(doc, "Table of Contents")
    toc_items = [
        ("1.", "Introduction"),
        ("2.", "Motivation / Need of the Study"),
        ("3.", "Literature Survey"),
        ("4.", "Problem Statement and Objectives"),
        ("5.", "Details of Study"),
        ("", "    5.1  The Transformer Architecture"),
        ("", "    5.2  BERT: Bidirectional Encoder Representations"),
        ("", "    5.3  GPT: Generative Pre-trained Transformer"),
        ("", "    5.4  Comparative Analysis"),
        ("", "    5.5  Practical Demonstration: RAG Pipeline"),
        ("6.", "Discussion on Results and Analysis"),
        ("7.", "Conclusion"),
        ("8.", "References"),
    ]
    for num, title in toc_items:
        p = doc.add_paragraph()
        text = f"{num} {title}" if num else title
        run = p.add_run(text)
        set_font(run, size=12, bold=bool(num))
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    add_blank(doc, 1)

    # List of Figures
    p = doc.add_paragraph()
    run = p.add_run("List of Figures")
    set_font(run, size=12, bold=True)
    p.paragraph_format.space_after = Pt(6)
    for fig in ["Figure 1: Transformer Architecture",
                "Figure 2: BERT vs GPT Architecture Comparison",
                "Figure 3: RAG Pipeline \u2014 BERT + GPT Working Together"]:
        p = doc.add_paragraph()
        run = p.add_run(fig)
        set_font(run, size=12)
        p.paragraph_format.space_after = Pt(3)

    add_blank(doc, 1)

    # List of Tables
    p = doc.add_paragraph()
    run = p.add_run("List of Tables")
    set_font(run, size=12, bold=True)
    p.paragraph_format.space_after = Pt(6)
    for tbl in ["Table 1: BERT vs GPT Feature Comparison",
                "Table 2: Task-wise Performance Comparison"]:
        p = doc.add_paragraph()
        run = p.add_run(tbl)
        set_font(run, size=12)
        p.paragraph_format.space_after = Pt(3)

    doc.add_page_break()

    # ==== CHAPTER 1: INTRODUCTION ====
    add_chapter_title(doc, "Chapter 1: Introduction")
    add_body_multi(doc, INTRODUCTION)

    # ==== CHAPTER 2: MOTIVATION ====
    add_chapter_title(doc, "Chapter 2: Motivation / Need of the Study")
    add_body_multi(doc, MOTIVATION)

    # ==== CHAPTER 3: LITERATURE SURVEY ====
    add_chapter_title(doc, "Chapter 3: Literature Survey")
    add_body_multi(doc, LITERATURE_SURVEY)

    # ==== CHAPTER 4: PROBLEM STATEMENT AND OBJECTIVES ====
    add_chapter_title(doc, "Chapter 4: Problem Statement and Objectives")
    add_section_heading(doc, "4.1 Problem Statement")
    add_body_multi(doc, PROBLEM_STATEMENT)
    add_section_heading(doc, "4.2 Objectives")
    for obj in OBJECTIVES:
        add_bullet(doc, obj)

    # ==== CHAPTER 5: DETAILS OF STUDY ====
    add_chapter_title(doc, "Chapter 5: Details of Study")
    add_section_heading(doc, "5.1 The Transformer Architecture")
    add_body_multi(doc, SECTION_5_1)
    add_figure(doc, FIG1_PATH, "Transformer Architecture (Vaswani et al., 2017)", 1)

    add_section_heading(doc, "5.2 BERT: Bidirectional Encoder Representations")
    add_body_multi(doc, SECTION_5_2)

    add_section_heading(doc, "5.3 GPT: Generative Pre-trained Transformer")
    add_body_multi(doc, SECTION_5_3)
    add_figure(doc, FIG2_PATH, "BERT vs GPT Architecture Comparison", 2)

    add_section_heading(doc, "5.4 Comparative Analysis")
    add_body_multi(doc, SECTION_5_4)
    add_table_with_data(doc, ["Feature", "BERT", "GPT"],
                        COMPARISON_TABLE, "BERT vs GPT Feature Comparison", 1)

    add_section_heading(doc, "5.5 Practical Demonstration: RAG Pipeline")
    add_body_multi(doc, SECTION_5_5)
    add_figure(doc, FIG3_PATH, "RAG Pipeline \u2014 BERT + GPT Working Together", 3)

    # ==== CHAPTER 6: RESULTS AND ANALYSIS ====
    add_chapter_title(doc, "Chapter 6: Discussion on Results and Analysis")
    add_body_multi(doc, RESULTS_DISCUSSION)
    add_table_with_data(doc, ["NLP Task", "Better Model", "Reason"],
                        TASK_TABLE, "Task-wise Performance Comparison", 2)

    # ==== CHAPTER 7: CONCLUSION ====
    add_chapter_title(doc, "Chapter 7: Conclusion")
    add_body_multi(doc, CONCLUSION)

    # ==== CHAPTER 8: REFERENCES ====
    add_chapter_title(doc, "Chapter 8: References")
    for i, ref in enumerate(REFERENCES, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(f"[{i}] {ref}")
        set_font(run, size=11)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # ==== SAVE ====
    doc.save(OUTPUT_PATH)
    print(f"\nSeminar Report saved to: {OUTPUT_PATH}")
    print("Generation complete!")


if __name__ == '__main__':
    create_report()
