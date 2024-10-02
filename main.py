import streamlit as st
import random
from backend import interpret_command_with_gpt, process_interpreted_command, write_assistant_response

# Function to display a soothing message to the user
def display_welcome_message():
    st.markdown("<h2 style='text-align: center;'>🌼 Welcome to AuraAI</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>I'm here to listen and support you. How can I help today?</h5>", unsafe_allow_html=True)

# Function to display the logo
def display_logo():
    logo_path = "./logo.png"  # Update this to the correct file path
    try:
        st.image(logo_path, width=100)  # Adjust width as necessary
    except FileNotFoundError:
        st.error("Logo image not found. Please check the file path.")

# Function to display quick response buttons
def display_quick_responses():
    st.markdown("### Quick Responses")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("I feel anxious"):
            return "I feel anxious"
    with col2:
        if st.button("I need someone to talk to"):
            return "I need someone to talk to"
    with col3:
        if st.button("Tell me something positive"):
            return "Tell me something positive"
    return None

# Initialize session state for messages, chatbot visibility, and context
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False
if "context" not in st.session_state:
    st.session_state.context = ""  # Initialize context to store conversation history

# Page configuration
st.set_page_config(page_title="AuraAI - Emotional Support Chatbot", layout="wide")

# Display the logo
display_logo()

# Title of the app and welcome message
display_welcome_message()

# Button to start chatting with the bot
if st.button("Start Chatting"):
    st.session_state.show_chatbot = True
    response = "Hi there, I'm here to help. How can I assist you today?"
    st.session_state.messages.append({"role": "assistant", "content": {"response": response}})
    st.session_state.context += f"Bot: {response}\n"  # Add response to the context

# Display the chatbot interface once the chat starts
if st.session_state.show_chatbot:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"]["response"], unsafe_allow_html=True)

    # User prompt input
    if prompt := st.chat_input("What’s on your mind?"):
        with st.chat_message("user"):
            st.markdown(f"{prompt}", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": {"response": prompt}})
        st.session_state.context += f"User: {prompt}\n"

        # Interpret the command with GPT, passing the full conversation context
        full_prompt = f"Previous chat context: {st.session_state.context}\n\nCurrent message: {prompt}"
        interpreted_command = interpret_command_with_gpt(full_prompt)

        # Process the interpreted command (generates response)
        response = process_interpreted_command(interpreted_command)
        st.session_state.context += f"Bot: {response['response']}\n"

        # Display the assistant's response with typing animation
        write_assistant_response(response["response"])

    # Display quick response buttons
    quick_response = display_quick_responses()
    if quick_response:
        with st.chat_message("user"):
            st.markdown(quick_response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": {"response": quick_response}})
        st.session_state.context += f"User: {quick_response}\n"

        # Interpret and process the quick response
        full_prompt = f"Previous chat context: {st.session_state.context}\n\nCurrent message: {quick_response}"
        interpreted_command = interpret_command_with_gpt(full_prompt)
        response = process_interpreted_command(interpreted_command)
        st.session_state.context += f"Bot: {response['response']}\n"

        # Display the assistant's response
        write_assistant_response(response["response"])

    # Like/Dislike Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Like"):
            st.success("Thanks for the feedback!")
    with col2:
        if st.button("👎 Dislike"):
            st.error("Sorry to hear that!")
