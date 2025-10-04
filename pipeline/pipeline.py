from indexer import *
from retriever import *
from response_generator import *
import argparse

def main():
    # Step1: index the raw documents into the vector db 
    # indexer()

    # Step2: fetch the query from termial command 
    # Will be replaced with actual frontend in industrial practice
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type = str, help = "Your query")
    args = parser.parse_args()
    query = args.query_text

    # Step3: use the query to fetch relevant context from the vector db
    if not retriever(query):
        generate_response(query, None)
        return

    context, results = retriever(query)

    # Step4: Generate and refine the final response and print it out 
    response = generate_response(query, context)

    # format and attach the source
    sources = ""
    i = 1
    for doc, _ in results:
        source = doc.metadata.get("source", None)
        exerpt = doc.page_content[:200]
        reference = f'[{i}] from \"{exerpt}\" in {source}'
        sources += reference
        i += 1

    print("Here is the response!\n")
    print(response)
    print("sources: \n", sources)

if __name__ == "__main__":
    main()



    