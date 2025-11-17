from typing import Optional, Annotated
from typing_extensions import TypedDict
from langgraph.graph import add_messages

class State(TypedDict):
    chat_history: Annotated[list, add_messages] # List of messages in the chat history
    #{'role': 'user', 'content': 'Hello!'}
    query: str # Current user query
    context: Optional[list[str]] # Context for the current query
    response: str # Response to the current query
    rewritten_query: str # Rewritten version of the current query
    
