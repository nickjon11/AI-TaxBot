from connect import getTokenLength
from langchainMain import sendMessage 
import streamlit as st
import openai
import numpy as np
import os

#UNUSED. This was our first interface, but we chose gradio over this.


# Page Layout
st.set_page_config(layout="wide")
# Theme (not working atm) - will need to revisit
primaryColor="#FF4B4B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#31333F"
font="sans serif"

# Top Navigation Bar (needs button functions)
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
col1.write("### Omega Team")
if col2.button("File Taxes"):
    st.session_state.page = os.path.abspath(__file__) 

col3.write("### How to use Chatbot (Needs a button function)")

if col4.button("Account"):
    st.session_state.page = "env/Scripts/Streamlit/pages/account.py" #Hardcoded Need to fix

# Image Uploader
col1, col2 = st.columns([6, 1])
col1.write("### Chatroom")
col2.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

# Information Table
st.write("### Tax Filing Information")
cols = st.columns(7)
labels = ["Country", "State", "Dependents", "Filing Status", "Total Income", "Total Deductions", "View Full Details"]
for col, label in zip(cols, labels):
    col.write(f"**{label}**")

#introduce self as AI Taxbot


# Suggested Responses
st.write("### Suggested Questions to Ask")
st.text("1. How do I file my taxes?")
st.text("2. What deductions am I eligible for?")
st.text("3. How do I check my filing status?")

# Chatbot Space (Requires OpenAI)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    #Start with an introductory message
    response = sendMessage(previousMessages = None)
    ai_response = response['messages'][-1].content
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user
user_input = st.chat_input("Ask our tax chatbot stuff:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = sendMessage(previousMessages = None, message = user_input) #send user question
    ai_response = response['messages'][-1].content

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    
def run():
    import subprocess
    subprocess.run(["streamlit", "run", os.path.abspath(__file__)])  #Run application

if __name__ == '__main__':
    from streamlit import runtime
    if not (runtime.exists()):
        run()