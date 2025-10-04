from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os
import shutil
from langchain_openai import OpenAIEmbeddings


DATA_PATH = "data"
CHROMA_PATH = "my_vector_db"
open_ai_key = os.environ["OPEN_AI_API_KEY"]


def indexer():

    loader = DirectoryLoader(DATA_PATH, glob = "*.pdf")
    documents = loader.load()

    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100
    )

    chunks = spliter.split_documents(documents)
    
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        
    db = Chroma.from_documents(chunks, 
                               embedding_function = OpenAIEmbeddings(), 
                               persist_directory = CHROMA_PATH)
    db.persist()
