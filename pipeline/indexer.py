from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
import os
import shutil
from pathlib import Path
from langchain_openai import OpenAIEmbeddings


DATA_PATH = "../data"
CHROMA_PATH = "my_vector_db"
open_ai_key = os.environ["OPENAI_API_KEY"]


def indexer():

    folder = Path(DATA_PATH)
    documents = []

    for pdf_path in folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())

    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100
    )

    chunks = spliter.split_documents(documents)
    
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        
    db = Chroma.from_documents(chunks, 
                               embedding = OpenAIEmbeddings(), 
                               persist_directory = CHROMA_PATH)
    # db.persist()
