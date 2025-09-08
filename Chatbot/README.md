# 🤖 Chatbot with Hugging Face & Ollama (LangChain)

This repository contains two Python implementations of a simple chatbot using different frameworks.  
It demonstrates how to build, run, and compare chatbot pipelines with **Hugging Face Transformers** and **LangChain + Ollama**.

---

## 📂 Files

### 1. `deepseek_huggingface.py`
- Downloads and loads a **DeepSeek model** from Hugging Face.
- Uses `transformers` and `AutoTokenizer` for tokenization and inference.
- Runs local text generation directly from pre-trained models.

### 2. `deepseek_ollama.py`
- Implements a chatbot pipeline using **LangChain** with **Ollama** as the backend.
- Showcases modular design for building advanced chatbot applications.
- Easily extendable with tools, custom prompts, or external APIs.

---

## 🔑 Key Highlights
- Compare **direct Hugging Face usage** vs. **LangChain pipeline integration**.
- Learn trade-offs in **deployment**, **flexibility**, and **application integration**.
- Provides a starting point for both **research experiments** and **practical chatbot projects**.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Run Chatbot
```
streamlit run deepseek_huggingface.py
```
OR
```
python deepseek_ollama.py
```




