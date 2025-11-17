from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface.embeddings import HuggingFaceEmbeddings  
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from models import State
from dotenv import load_dotenv
from prompts import REWRITE_PROMPT, SYSTEM_PROMPT, query_rewrite_extend, system_prompt_extend
import os

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp", 
    temperature=0,
    convert_system_message_to_human=True
)
def retriever_agent(state: State):
    user_input = state.get("rewritten_query")

    # Initialize the embedding model
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
        ) 
    # Initialize the vector database
    vdb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding
        )
    
    #create retriever from vector database
    retriever = vdb.as_retriever( search_kwargs={"k":10})
    result = retriever.invoke(user_input)

    return{
        "context": result
    }

def rewrite_query_agent(state: State):
    user_input = state.get("query")
    chat_history = state.get("chat_history")

    messages = [
        SystemMessage(content=REWRITE_PROMPT),
        HumanMessage(content=query_rewrite_extend(user_input, chat_history))
    ]
    response = llm.invoke(messages)
    rewritten_query = response.content.strip()
    return {
        "rewritten_query": rewritten_query
    }

def response_agent(state: State):
    user_input = state.get("rewritten_query")
    chat_history = state.get("chat_history")
    context = state.get("context")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=system_prompt_extend(user_input, str(chat_history), str(context)))
    ]
    response = llm.invoke(messages)
    final_response = response.content.strip()
    return {
        "response": final_response
    }

