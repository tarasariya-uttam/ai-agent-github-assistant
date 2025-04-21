import os
import sys
import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.ingest.github_loader import GitHubLoader
from backend.vector_store.vector_store import VectorStore
from backend.chains.qa_chain import QAChain

load_dotenv()

st.set_page_config(
    page_title="Git Repo Analysis Bot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        margin-left: 20%;
        border: 1px solid #e0e0e0;
    }
    .chat-message.assistant {
        margin-right: 20%;
        border: 1px solid #e0e0e0;
    }
    .chat-message .content {
        width: 100%;
    }
    .thinking-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Git Repo Analysis Bot 🤖")
st.markdown("""
**Analyze any GitHub repository using AI. Ask about structure, key modules, setup steps, and recent changes — all answered in real-time using GPT-4, LangChain, and RAG.**  
**Built to tackle the challenge of deeply understanding large codebases and commit history with clean, modular retrieval and embedding pipelines.**
""")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None
if "question" not in st.session_state:
    st.session_state.question = ""
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

with st.sidebar:
    st.header("Repository Settings")
    repo_url = st.text_input("Enter GitHub Repository URL:")
    
    if repo_url and repo_url != st.session_state.current_repo:
        try:
            with st.spinner("Loading repository content..."):
                loader = GitHubLoader()
                content = loader.get_repo_content(repo_url)
                
                vector_store = VectorStore()
                vector_store.create_vector_store(content)
                st.session_state.vector_store = vector_store
                
                qa_chain = QAChain()
                qa_chain.create_chain(vector_store.get_retriever())
                st.session_state.qa_chain = qa_chain
                
                st.session_state.current_repo = repo_url
                st.session_state.conversation = []
                st.session_state.question = ""
                st.session_state.is_thinking = False
                
                st.success("Repository loaded successfully!")
                
        except Exception as e:
            st.error(f"Error loading repository: {str(e)}")

if st.session_state.qa_chain:
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="content">
                    <strong>You:</strong><br>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant">
                <div class="content">
                    <strong>Assistant:</strong><br>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if "sources" in message:
                with st.expander("View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}**")
                        st.text(source)
                        st.markdown("---")
    
    if st.session_state.is_thinking:
        st.markdown("""
        <div class="thinking-container">
            <div style="text-align: center;">
                <div class="stSpinner">
                    <div class="spinner"></div>
                </div>
                <p style="margin-top: 10px;">Thinking...</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def handle_question():
        question = st.session_state.question
        if question:
            st.session_state.conversation.append({"role": "user", "content": question})
            st.session_state.is_thinking = True
            
            try:
                result = st.session_state.qa_chain.get_answer(question)
                
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"]
                })
                
                st.session_state.question = ""
                st.session_state.is_thinking = False
                
            except Exception as e:
                st.error(f"Error getting answer: {str(e)}")
                st.session_state.is_thinking = False
    
    st.text_input(
        "Ask a question about the repository...",
        key="question",
        on_change=handle_question
    )
else:
    st.info("Please enter a GitHub repository URL in the sidebar to get started.") 