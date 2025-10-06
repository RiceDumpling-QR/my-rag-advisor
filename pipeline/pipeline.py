import warnings, sys, os, contextlib, argparse

warnings.filterwarnings("ignore")

with contextlib.redirect_stdout(open(os.devnull, "w")), contextlib.redirect_stderr(open(os.devnull, "w")):
    from indexer import *
    from retriever import *
    from response_generator import *


def main():

    warnings.filterwarnings("ignore")

    # Step1: fetch the query from termial command 
    # Will be replaced with actual frontend in industrial practice
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type = str, help = "Your query")
    parser.add_argument("-r", "--reset", action = "store_true", help = "Rebuild the database before running")
    args = parser.parse_args()
    query = args.query_text

    # Step2: index the raw documents into the vector db depending on reset or not
    if args.reset:
        print("Waiting for the new database to load ...")
        indexer()

    # Step3: use the query to fetch relevant context from the vector db
    if not retriever(query):
        print("Waiting for a response ...")
        generate_response(query, None)
        return

    context, results = retriever(query)

    # Step4: Generate and refine the final response and print it out 
    print("Waiting for a response ...")
    response = generate_response(query, context)

    # format and attach the source
    sources = ""
    i = 1
    for doc, _ in results:
        source = doc.metadata.get("source", None)
        exerpt = doc.page_content[:200]
        reference = f'[{i}] from \"{exerpt}\" in {source}...\n'
        sources += reference
        i += 1

    print("Here is the response!")
    print(response)
    print("sources: \n", sources)

if __name__ == "__main__":
    main()



    