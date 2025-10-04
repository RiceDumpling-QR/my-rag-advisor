from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from indexer import *

def retriever(query_text):
    db = Chroma(persist_directory = CHROMA_PATH, embedding_function = OpenAIEmbeddings())
    results = db.similarity_search_with_relevance_scores(query_text, 3)

    if(len(results) == 0 or results[0][1] < 0.7):
        return None

    context = ""
    for document, _relevancy_score in results:
        context += "\n"
        context += document.page_content
    
    return (context, results)