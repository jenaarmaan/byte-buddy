# app.py
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import streamlit as st
import os
import google.generativeai as genai

# Load Google API key from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_box = st.text_input("Input: ", key="input")
submit_button = st.button("Ask the question")

if submit_button and input_box:
    response = get_gemini_response(input_box)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_box))
    st.subheader("The Response is")
    st.write(response)
    st.session_state['chat_history'].append(("Bot", response))
else:
    st.write("Please enter a question and click 'Ask the question'!")

st.subheader("The Chat History is")
chat_history_text = ""
for role, text in st.session_state['chat_history']:
    chat_history_text += f"{role}: {text}\n"
st.text_area("Chat History", value=chat_history_text, height=200)