import streamlit as st
from workflow import Workflow
from models import State
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("Museum Guide Chatbot 🏛️")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

if prompt := st.chat_input("Ask me anything about Egyptian civilization museum!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    # generate response
    with st.chat_message("assistant"):
        chat_history = [HumanMessage(content=msg['content']) for msg in st.session_state.messages]
        initial_state = State(
            chat_history=chat_history,
            query=prompt,
            context=None,
            response="",
            rewritten_query=""
        )

        result = Workflow().run(initial_state)
        response = result.get("response", "I am sorry, I don't have the information you need right now.")
        st.markdown(response)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response
        })
