from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
import os
import shutil
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
import requests
from langchain.schema import Document



CHROMA_PATH = "my_vector_db"
open_ai_key = os.environ["OPENAI_API_KEY"]
fb_token = os.environ["ACCESS_TOKEN"]


def indexer():

    # load pdfs
    pdf_path = "../data/pdf"
    pdf_file_path = Path(pdf_path)
    pdf_docs = []

    for pdf_path in pdf_file_path.glob("*.pdf"):
        pdf_loader = PyPDFLoader(str(pdf_path))
        pdf_docs.extend(pdf_loader.load())
    
    # load md files
    md_file_path = "../data/md"

    md_loader = DirectoryLoader(md_file_path, glob = "*.md")
    md_docs = md_loader.load()

    documents = pdf_docs + md_docs

    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100
    )

    chunks = spliter.split_documents(documents)
    
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        
    Chroma.from_documents(chunks, 
                        embedding = OpenAIEmbeddings(), 
                        persist_directory = CHROMA_PATH)


if __name__ == "__main__":
    indexer()