import streamlit as st
import random
import time

st.title("Streamlit Basics")

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    return response

# display chat messages from history

# In the above snippet, we've added a title to our app and a for loop to
#  iterate through the chat history and display each message in the chat 
#  message container (with the author role and message content). 
#  We've also added a check to see if the messages key is in st.session_state. 
#  If it's not, we initialize it to an empty list. 
#  This is because we'll be adding messages to the list later on, and 
#  we don't want to overwrite the list every time the app reruns.

with st.sidebar.title("Sidebar"):
    st.write("Hello !!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("what's up")

if prompt:
    print("user prompted", prompt)
    print("response_generator()", response_generator())
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "Agent", "content": response_generator()})

