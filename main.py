import streamlit as st
from langchain_ollama import OllamaLLM
import time
import base64

# Set page config
st.set_page_config(page_title="PyBot", page_icon="🐍", layout="wide")

# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image
background_image = get_base64_of_bin_file('bg.avif')


# Custom CSS to improve the look
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
</style>
""", unsafe_allow_html=True)


model = OllamaLLM(model="llama3")

def get_response(user_input):
    if user_input:
        result = model.invoke(input=user_input)
        return result
    else:
        return "Please ask your Python-related query."

st.title("🐍 PyBot: Your Python Coding Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask your Python question here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = get_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.title("About PyBot")
    st.write("PyBot is your AI assistant for Python-related coding questions. Feel free to ask about:")
    st.write("- Python syntax")
    st.write("- Code optimization")
    st.write("- Best practices")
    st.write("- Library usage")
    st.write("- Debugging tips")
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()