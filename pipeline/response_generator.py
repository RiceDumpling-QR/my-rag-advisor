from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


def generate_response(query, context):
    # load the chat model and fetch reponse only from query if no context
    model = ChatOpenAI(model = "gpt-4", temperature = 0.7)
    
    if not context:    
        print("This query is not relevant to the context.\n")
        print("fetching response from general knowledge ... response: ", 
                model.invoke(query))
        
    # if we have both context and theory then use the built in to buil up prompt
    tpl = "Ask {question} using the context {context}"
    prompt = PromptTemplate(input_variables = ["question", "context"], 
                            template = tpl)
    filled_prompt = prompt.format(question = query, context = context)


    response = model.invoke(filled_prompt).content
    
    return response