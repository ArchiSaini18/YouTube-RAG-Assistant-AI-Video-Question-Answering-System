### ▶ YouTube RAG Assistant – AI Video Question Answering System

An AI-powered YouTube video assistant that allows users to ask questions about any YouTube video and receive answers generated directly from the video transcript using Retrieval-Augmented Generation (RAG).

The system automatically:

- Extracts video transcripts

- Splits them into semantic chunks

- Creates embeddings

- Stores them in a FAISS vector database

- Retrieves relevant context

- Generates answers using a HuggingFace LLM

- Built with LangChain, FAISS, HuggingFace Models, and Streamlit.

## 🚀 Live Application

👉 Direct View / Try the App:
https://youtube-rag-assistant-ai-video-question-answering-system-vygvt.streamlit.app/

### 🎯 Quick Links

- Overview

- Features

- Installation

- Quick Start

- Web App Interface

- Implementation Details

- RAG Architecture

- Dataset & Processing

- Example Outputs

- Improvements

- Troubleshooting

### 📌 Overview

YouTube RAG Assistant is a smart AI application that enables users to interactively chat with a YouTube video.

Instead of manually watching long videos, users can simply ask questions and receive accurate answers grounded in the video transcript.

This project demonstrates a complete Retrieval-Augmented Generation pipeline using:

- LangChain

- HuggingFace LLMs

- FAISS Vector Database

- YouTube Transcript API

- Streamlit Web Interface

### 🚀 Key Achievements

✅ Full RAG pipeline implementation

✅ Automatic transcript extraction from YouTube

✅ Vector similarity search with FAISS

✅ LLM-powered contextual answers

✅ Interactive Streamlit web interface

✅ Custom UI design with CSS

✅ Real-time question answering

✅ Expandable architecture for other content sources

### ✨ Features
🧠 AI & RAG Features

- Automatic YouTube transcript extraction

- Text chunking for semantic retrieval

- SentenceTransformer embeddings

- FAISS similarity search

- Context-aware LLM answer generation

- HuggingFace model integration

- Adjustable temperature and token limits

### 🌐 Web Application Features
### 📝 User Inputs

- Users can configure:

- HuggingFace API Token

- LLM Model ID

- Max Tokens

- Temperature

- YouTube Video URL or ID

- Chunk Size

- Chunk Overlap

- Top-K Retrieval

### ⚙️ Retrieval Settings

Users can customize:

- Transcript chunk size

- Chunk overlap

- Number of retrieved chunks

- Embedding model

This helps improve retrieval accuracy and answer quality.

### 💬 Chat Interface

Users can:

- Ask questions about the video

- Receive context-aware answers

- View conversation history

- Clear chat history

### 🎨 Web App Interface
Left Panel — Configuration

Users configure:

- HuggingFace Token

- LLM Model

- Video URL

- Retrieval settings

Then click:

### Load Video & Build Index

### Right Panel — Chat Interface

Displays:

- Video status

- Conversation history

- Question input

- AI-generated responses

### 🛠 Installation
- Prerequisites

- Python 3.9+

- pip

- 4GB RAM minimum

- HuggingFace API Token

### Step 1 — Clone Repository
git clone https://github.com/yourusername/youtube-rag-assistant.git
cd youtube-rag-assistant

### Step 2 — Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

### Step 3 — Install Dependencies
pip install -r requirements.txt
▶ Quick Start

Run the Streamlit app:

streamlit run app.py

### Open browser:

http://localhost:8501
🧠 RAG System Architecture

The system follows the Retrieval-Augmented Generation pipeline.

### Step 1 — Transcript Extraction

The system retrieves subtitles using:

- YouTubeTranscriptApi

- Example transcript:

Deep learning models are inspired by the human brain...

### Step 2 — Text Chunking

Transcript is split into smaller segments using:

- RecursiveCharacterTextSplitter

- This improves retrieval accuracy.

Example:

Chunk 1: Introduction to neural networks
Chunk 2: Types of neural networks
Chunk 3: Applications of CNNs

### Step 3 — Embedding Generation

Each chunk is converted into vector embeddings using:

- sentence-transformers/all-MiniLM-L6-v2

- This allows semantic similarity search.

### Step 4 — Vector Storage

- Embeddings are stored in:

- FAISS Vector Database

- FAISS enables fast nearest-neighbor retrieval.

### Step 5 — Context Retrieval

When a question is asked:

- The question is embedded

- FAISS finds Top-K relevant chunks

- Retrieved context is sent to the LLM

### Step 6 — Answer Generation

The retrieved context and question are passed to the LLM.

Example prompt:

You are a helpful assistant.
Answer only from the provided transcript.

Context:
{context}

Question:
{question}

The model generates a grounded response.

### 📊 Example Usage
Example 1

User Question

What are the types of neural networks discussed?

AI Answer

The video discusses five types of neural networks:
1. Feedforward Neural Networks
2. Convolutional Neural Networks
3. Recurrent Neural Networks
4. Autoencoders
5. Generative Adversarial Networks

### Example 2

User Question

What is the main idea behind convolutional neural networks?

AI Answer

Convolutional neural networks are designed to process grid-like data such as images.
They use convolutional filters to detect patterns like edges, textures, and shapes.

### 🔧 System Requirements

Requirement	Minimum	Recommended
RAM	4 GB	8 GB
Disk Space	300 MB	1 GB
Python	3.9	3.11

### 🚀 Potential Improvements
### Model Enhancements

- Use embedding models like BGE or Instructor

- Add reranking models

- Integrate OpenAI or Llama models

### Retrieval Improvements

- Hybrid search (BM25 + embeddings)

- Metadata filtering

- Dynamic chunking

### UI Enhancements

- Video preview player

- Highlight retrieved transcript sections

- Export answers to PDF

- Save conversation history

### 🧪 Future AI Upgrades

- Multi-video knowledge base

- Podcast & lecture indexing

- Meeting transcription QA

- GPT-based summarization

- Automatic chapter detection

### 🛠 Troubleshooting
- Missing Module Error

Install dependencies:

pip install -r requirements.txt

### Transcript Not Available

Some videos disable subtitles.

Solution:

- Choose a video with captions enabled.

FAISS Installation Issue

Install CPU version:

pip install faiss-cpu
✅ Evaluation Criteria Met

✔ Full RAG implementation
✔ Clean modular architecture
✔ Professional UI design
✔ Real-world AI application
✔ Interactive question answering system
✔ Expandable project structure

### 📚 Tech Stack

- Python

- LangChain

- HuggingFace Models

- FAISS

- Sentence Transformers

- Streamlit

- YouTube Transcript API

### 👨‍💻 Author

Archi Saini

AI / Machine Learning Enthusiast
Projects focused on LLMs, RAG systems, and AI applications
