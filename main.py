import streamlit as st 
import time
import base64
from dotenv import load_dotenv
import os
import requests
import json
import warnings

warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

st.set_page_config(page_title="PyBot", page_icon="🐍", layout="wide")

# Function to load a background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = get_base64_of_bin_file('bg.avif')

# Styling
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image}");
        background-size: cover;
    }}
    .stTextInput > div > div > input {{
        background-color: rgba(240, 242, 246, 0.7);
    }}
    .stButton > button {{
        width: 100%;
        background-color: rgba(76, 175, 80, 0.7);
        color: white;
    }}
    .chat-message {{
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }}
    .chat-message.user {{
        background-color: rgba(43, 49, 62, 0.7);
    }}
    .chat-message.bot {{
        background-color: rgba(71, 80, 99, 0.7);
    }}
    .stApp > header {{
        background-color: rgba(0, 0, 0, 0.5);
    }}
    .stSidebar > div:first-child {{
        background-color: rgba(0, 0, 0, 0.7);
    }}
</style>
""", unsafe_allow_html=True)

# Fetch response using Groq API
def get_response_from_groq(user_input):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a world-class Python developer assistant. Please provide concise, Python-related responses."},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(
            url="https://api.groq.com/v1/chat/completions",  # Replace with the actual Groq API endpoint
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        if "choices" in data:
            return data['choices'][0]['message']['content']
        else:
            return "Unexpected response format. Please check the API response."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Main Interface
st.title("🐍 PyBot: Your Python Coding Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Input handling
if prompt := st.chat_input("Ask your Python question here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Fetch and display response
    response = get_response_from_groq(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.title("About PyBot")
    st.write("PyBot is your AI assistant for Python-related coding questions. Feel free to ask about:")
    st.write("- Python syntax")
    st.write("- Code optimization")
    st.write("- Best practices")
    st.write("- Library usage")
    st.write("- Debugging tips")
    st.divider()
    st.subheader("Developer")
    st.write("Paavan Shetty")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/paavan-shetty-419667259/)")
    with col2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/paavanshetty23)")
