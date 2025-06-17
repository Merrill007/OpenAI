import streamlit as st
import openai

# Configure the page
st.set_page_config(
    page_title="Futuristic Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container {
        background: #1a1a2e;
        color: #e94560;
    }
    h1 {
        color: #e94560;
    }
    .stTextInput > div > div > input {
        background-color: #0f3460;
        color: #e94560;
        border: 1px solid #e94560;
    }
    .chat-response {
        margin-top: 20px;
        padding: 10px;
        background-color: #0f3460;
        color: #e94560;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🤖 Futuristic Chatbot")

# Load OpenAI key securely
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Check API key
if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets.")
    st.stop()

# Maintain session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.text_input("Say something:")

# Generate response
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            st.error(f"An error occurred: {e}")
            reply = "Sorry, I couldn’t generate a response."

    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display full conversation
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"<div class='chat-response'>🤖: {message['content']}</div>", unsafe_allow_html=True)
