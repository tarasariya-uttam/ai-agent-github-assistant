import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-ada-002"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None
    
    def prepare_documents(self, content: Dict) -> List[str]:
        """Prepare documents from repository content."""
        documents = []
        
        # Add README
        if content["readme"]:
            documents.append(f"README.md:\n{content['readme']}")
        
        # Add all files with their types
        for file in content["files"]:
            file_type = file["type"].upper()
            documents.append(f"File: {file['path']} (Type: {file_type})\nContent:\n{file['content']}")
        
        # Add commit history
        commit_text = "Recent Commits:\n"
        for commit in content["commit_history"]:
            commit_text += f"Commit: {commit['sha']}\nMessage: {commit['message']}\nDate: {commit['date']}\n\n"
        documents.append(commit_text)
        
        return documents
    
    def create_vector_store(self, content: Dict):
        """Create FAISS vector store from repository content."""
        documents = self.prepare_documents(content)
        texts = self.text_splitter.split_text("\n\n".join(documents))
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
    
    def get_retriever(self, k: int = 4):
        """Get retriever from vector store."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        return self.vector_store.as_retriever(search_kwargs={"k": k}) 