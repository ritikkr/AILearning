import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os

## Page config

st.set_page_config(page_title="Q&A Chatbot with Groq", page_icon="🤖")


#Title
st.title("🤖 Q&A Chatbot with Groq and LangChain")
st.markdown("This is a simple Q&A chatbot built using LangChain and Groq's chat model.")

## sidebar
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key.")
    model_name = st.selectbox("Select Model", options=["llama-3.1-8b-instant", "llama-3.3-70b-versatile"], 
                              index=0, 
                              
                              help="Choose the Groq chat model to use.")
    # clear button
    if st.button("Clear Chat History"):
        st.session_state['messages'] = []
        st.rerun()

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Initialize Groq chat model
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
        return None
    # Initialize and return the Groq chat model
    llm = ChatGroq(api_key=api_key, model=model_name, temperature=0.7, streaming=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions based on provided context."),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain

## get chain 
chain = get_chain(groq_api_key, model_name)

if not chain:
    st.warning("Please provide a valid Groq API key to initialize the chatbot.")
    st.markdown("You can get your API key from the [Groq Console](https://console.groq.com).")
else:
    ## display chat messages from history
    for msg in st.session_state['messages']:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    # User input
    if question := st.text_input("Ask a question about the context:"):
        # Append user message to session state
        st.session_state['messages'].append({'role': 'user', 'content': question})

        with st.chat_message("user"):
            st.write(question)
        # Get response from Groq chat model
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # stream response from groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")  # cursor effect
                message_placeholder.markdown(full_response)  # final response without cursor

                # Append assistant message to session state
                st.session_state['messages'].append({'role': 'assistant', 'content': full_response})
            except Exception as e:
                message_placeholder.markdown("Error: " + str(e))
        
        





