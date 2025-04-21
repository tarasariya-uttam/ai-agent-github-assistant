# GitHub RAG Bot

A Retrieval Augmented Generation (RAG) bot that allows you to ask questions about any GitHub repository. The bot uses LangChain, OpenAI's GPT-4, and FAISS vector storage to provide accurate answers based on the repository's content.

## Features

- Fetch and analyze GitHub repository content (README, Python files, commit history)
- Create embeddings using OpenAI's embedding model
- Store and retrieve information using FAISS vector store
- Ask natural language questions about the repository
- View sources used to generate answers

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/github-rag-bot.git
cd github-rag-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
```

4. Run the Streamlit app:
```bash
streamlit run app/main.py
```

## Usage

1. Open the Streamlit app in your browser
2. Enter a GitHub repository URL in the sidebar
3. Wait for the repository content to be loaded
4. Ask questions about the repository in natural language
5. View answers and their sources

## Project Structure

```
github-rag-bot/
├── app/
│   └── main.py              # Streamlit UI
├── backend/
│   ├── ingest/
│   │   └── github_loader.py # GitHub content fetcher
│   ├── vector_store/
│   │   └── vector_store.py  # FAISS vector store
│   └── chains/
│       └── qa_chain.py      # LangChain QA chain
├── utils/                   # Utility functions
├── data/                    # Data storage
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Dependencies

- LangChain
- OpenAI
- FAISS
- Streamlit
- FastAPI
- PyGithub
- Python-dotenv

## License

MIT 