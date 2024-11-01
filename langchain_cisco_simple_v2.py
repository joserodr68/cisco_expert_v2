import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import hashlib

# Auxiliary function to hash any string
def hash_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

# The correct password hash (result of hashing in cyrilic)
CORRECT_PASSWORD_HASH = "29d2f49453c42ee55e67660289083e32"

# Set up the page configuration
st.set_page_config(
    page_title="Cisco Expert for Маришка v2",
    page_icon=":computer:",
    layout="centered",
    initial_sidebar_state="auto"
)

# Apply custom CSS styles
st.markdown(
    """
    <style>
        .stApp {
            background-color: #ADD8E6;  /* Light blue background */
        }
        .css-1d391kg {  /* Sidebar */
             background-color: #FEE338;  /* Matte yellow background */
        }
        .stTextInput, .stButton, .stNumberInput {
            margin-bottom: 10px;  /* Space between form elements */
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Initialize the session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display the title and background first
st.title("Cisco Expert for Маришка v2")

# Function to display the login form and handle login
def display_login():
    with st.form(key='login_form'):
        password = st.text_input("Enter password:", type="password")
        submit_button = st.form_submit_button(label="Login")
        if submit_button:
            if hash_string(password) == CORRECT_PASSWORD_HASH:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

# Function to display the main application content
def display_app():
    # Get the Groq API key from environment variables-- streamlit secrets (.streamlit/secrets.toml)
    api_key = st.secrets["GROQ_API_KEY"]
    

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
    Your responses should be factual, detailed, and include practical examples to ensure clarity.
    Important:  Your response in the same language than the user question. 
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

# Display either the login form or the main app based on login status
if st.session_state.logged_in:
    display_app()
else:
    display_login()
