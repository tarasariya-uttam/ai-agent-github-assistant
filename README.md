# GitHub AI Agent – Repository Assistant 🔍🤖

An intelligent assistant that lets you **chat with any public GitHub repo** using GPT-4. Ask about structure, setup steps, important modules, recent changes, or anything else — powered by **LangChain**, **RAG**, and **FAISS**.

---

## 🚀 Use Cases
- Understand complex GitHub repos instantly
- Ask about architecture, functions, or file roles
- Get summaries of recent commits or changes
- Assist onboarding devs or exploring open-source codebases

---


## 🛠 Tech Stack
- **LLM**: OpenAI GPT-4
- **Framework**: LangChain + RetrievalQA
- **Embedding**: OpenAI Embeddings
- **Vector Store**: FAISS
- **Frontend**: Streamlit
- **Backend**: Python, FastAPI
- **Data Source**: GitHub API

---

## 🧠 Workflow

1. Enter a GitHub repo URL  
2. Bot fetches: README, Python files, commit history  
3. All content is embedded and indexed  
4. Ask anything — LLM retrieves answers using RAG  
5. View answer + source files (optional)

---

## 📦 Project Structure
```
github-rag-assistant/
├── app/                   # Streamlit frontend
├── backend/
│   ├── ingest/            # GitHub data loader
│   ├── vector_store/      # Embedding + FAISS logic
│   └── chains/            # LangChain QA chain
├── utils/                 # Helper functions
├── data/                  # Local cache (gitignored)
├── .env                   # Your API keys (not pushed)
├── requirements.txt       # All dependencies
└── README.md              # You’re here
```

---

## ⚙️ Setup

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/github-rag-assistant.git
cd github-rag-assistant
```

2. **Create `.env` file** with:
```
OPENAI_API_KEY=your_key
GITHUB_TOKEN=your_token
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app/main.py
```

---

## 🙋 How to Use
- Paste a GitHub repo URL (e.g. https://github.com/psf/requests)
- Ask:  
  - “What is this repo for?”  
  - “List key modules”  
  - “How do I run this?”  
  - “What changed in the last 5 commits?”  

---

## 📄 License

MIT © [Uttamkumar Tarasariya](https://www.linkedin.com/in/uttamkumar-tarasariya-5759421b7/)
