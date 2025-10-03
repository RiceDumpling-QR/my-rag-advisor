from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os
import shutil
from langchain_openai import OpenAIEmbeddings


DATA_PATH = "data"
CHROMA_PATH = "my_vector_db"
open_ai_key = os.environ["OPEN_AI_API_KEY"]


def main():
    build_data_store()

def build_data_store():
    document = load_document()
    chunks = split_document(document)
    db = load_chunk_into_db(chunks)

def load_document():
    loader = DirectoryLoader(DATA_PATH, glob = "*.md")
    documents = loader.load()
    return documents

def split_document(documents):
    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100
    )

    chunks = spliter.split_documents(documents)
    return chunks


def load_chunk_into_db(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    db = Chroma.from_documents(chunks, 
                               embedding_function = OpenAIEmbeddings(), 
                               persist_directory = CHROMA_PATH)
    db.persist()
    return db 

if __name__ == "__main__":
    main()