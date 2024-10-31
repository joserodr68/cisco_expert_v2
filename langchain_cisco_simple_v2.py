# Required imports

import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

import time




load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Get the Groq API key from environment variables-- streamlit secrets (.streamlit/secrets.toml)
#api_key = st.secrets["GROQ_API_KEY"]


#pip install langchain-groq
# Set up the LLM with ChatGroq
llm = ChatGroq(
    temperature=0,
    api_key= api_key,
    model= 'llama-3.1-70b-versatile',
)

# Define system and human messages for the prompt
system = """You are a Cisco Systems networking specialist with deep knowledge of router and switching configurations. 
Your expertise also includes WiFi and Datacenter equipment.
Always aim to provide clear and precise configuration examples whenever possible.
Write the configuration examples as a block in markdown and explain separately.
If asked in russian, respond in russian, except for the configuration examples that should remain in english
Your responses should be factual, detailed, and include practical examples to ensure clarity.
"""

human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# Initialize memory for conversation history
memory = ConversationBufferMemory()

# Create a query engine
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# Function to handle chat predictions with memory
def predict(input, history):
    response = llm_chain.run(input)
    return response

# Streamlit interface

st.markdown(
        """
        <style>
            .stApp {
                background-color: #ADD8E6;  /* Fondo azul claro */ 
            }
            .css-1d391kg {  /* Sidebar */
                 background-color: #FEE338;  /* Fondo amarillo mate */
            }
            .stTextInput, .stButton, .stNumberInput {
                margin-bottom: 10px;  /* Espacio entre los elementos del formulario */
            }
        </style>
        """, 
        unsafe_allow_html=True
)

st.title("Cisco Expert for Маришка v2")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history
for message in st.session_state['chat_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input box for user query
user_input = st.chat_input("Ask a question about Cisco networking...")

if user_input:
    # Add user message to chat history
    st.session_state['chat_history'].append({'role': 'user', 'content': user_input})

    # Generate response
    response = predict(user_input, st.session_state['chat_history'])

    # Add response message to chat history
    st.session_state['chat_history'].append({'role': 'assistant', 'content': response})

    # Display the assistant's response
    with st.chat_message('assistant'):
        st.markdown(response)
