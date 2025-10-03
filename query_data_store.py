
import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os 

open_ai_key = os.environ["OPEN_AI_API_KEY"]

CHROMA_PATH = "my_vector_db"

def main():
    query_data_store()


def query_data_store():

    # first parse arguments -- get query
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type = str, help = "Your query")
    args = parser.parse_args()
    query_text = args.query_text


    # fetch the results back from the database -- get context
    db = Chroma(persist_directory = CHROMA_PATH, embedding_function = OpenAIEmbeddings())
    results = db.similarity_search_with_relevance_scores(query_text)
    context_text = ""
    for document, _relevancy_score in results:
        context_text += "\n\n"
        context_text += document.page_content

    # build up the prompt from the template
    tpl = "Ask {question} using the context {context}"
    prompt = PromptTemplate(input_variables = ["question", "context"], 
                            template = tpl)
    filled_prompt = prompt.format(question = query_text, context = context_text)

    # use the filled prompt to get the response from chat model
    model = ChatOpenAI(model = "gpt-4", temperature = 0.7)
    if(len(results) == 0 or results[0][1] < 0.7):
        print("This query is not relevant to the context.\n")
        print("fetching response from general knowledge ... response: ", 
              model.invoke(query_text))


    response = model.invoke(filled_prompt).content
    sources = []
    for doc, _ in results:
        sources.append(doc.metadata.get("source", None))

    print("Here is the response!\n")
    print(response)
    print("sources: \n", sources)

if __name__ == "__main__":
    main()

    




    



