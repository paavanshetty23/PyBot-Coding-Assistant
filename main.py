import streamlit as st 
import time
import base64
from dotenv import load_dotenv
import os
import requests
import json
import warnings

warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

load_dotenv()

# Use Groq API key 
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

st.set_page_config(page_title="PyBot", page_icon="🐍", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = get_base64_of_bin_file('bg.avif')

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
    .chat-message .avatar {{
      width: 20%;
    }}
    .chat-message .avatar img {{
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }}
    .chat-message .message {{
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }}
    .stApp > header {{
        background-color: rgba(0, 0, 0, 0.5);
    }}
    .stSidebar > div:first-child {{
        background-color: rgba(0, 0, 0, 0.7);
    }}
    .copy-button {{
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 2px 1px;
        cursor: pointer;
        border-radius: 4px;
    }}
    pre {{
        background-color: #333;
        color: #f8f8f2;
        padding: 10px;
        border-radius: 5px;
        position: relative;
        white-space: pre-wrap;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
function copyToClipboard(button, codeId) {
    const codeElement = document.getElementById(codeId);
    const text = codeElement.textContent;
    
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
        button.textContent = 'Copied!';
        setTimeout(function() {
            button.textContent = 'Copy';
        }, 2000);
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        button.textContent = 'Failed to copy';
    });
}
</script>
""", unsafe_allow_html=True)

# Groq LLM models
llm_providers = [
    'llama2-70b-4096',
    'mixtral-8x7b-32768', 
    'gemma-7b-it'
]

selected_llm = st.sidebar.selectbox("Select LLM Provider", llm_providers, index=0)

def get_response(user_input, selected_llm):
    messages = [
        {"role": "system", "content": "You are a world class Python developer assistant. Please provide concise, Python-related responses. When providing code, ensure proper indentation and formatting."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": selected_llm,
                "messages": messages,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        
        response_json = response.json()
        if 'choices' in response_json:
            return response_json['choices'][0]['message']['content'], selected_llm
        else:
            return f"Unexpected response format: {response_json}", None
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", None

def format_response(response):
    formatted_response = ""
    in_code_block = False
    code_block = ""
    code_block_count = 0
    for line in response.split('\n'):
        if line.strip().startswith("```"):
            if in_code_block:
                code_id = f"code-block-{code_block_count}"
                formatted_response += f'<pre><code id="{code_id}">{code_block.strip()}</code></pre>\n'
                formatted_response += get_copy_button(code_id, code_block_count) + '\n'
                in_code_block = False
                code_block = ""
                code_block_count += 1
            else:
                in_code_block = True
        elif in_code_block:
            code_block += line + '\n'
        else:
            formatted_response += line + '\n\n'

    if in_code_block:
        code_id = f"code-block-{code_block_count}"
        formatted_response += f'<pre><code id="{code_id}">{code_block.strip()}</code></pre>\n'
        formatted_response += get_copy_button(code_id, code_block_count) + '\n'

    return formatted_response

def get_copy_button(code_id, button_id):
    return f"""
    <button class="copy-button" onclick="copyToClipboard(this, '{code_id}')">Copy</button>
    """

st.title("🐍 PyBot: Your Python Coding Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask your Python question here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, model_used = get_response(prompt, selected_llm)
    formatted_response = format_response(response)

    with st.chat_message("assistant"):
        st.markdown(formatted_response, unsafe_allow_html=True)
        
        if model_used:
            st.info(f"Model used: {model_used}")
            
    st.session_state.messages.append({"role": "assistant", "content": formatted_response})

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
