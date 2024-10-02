import json
import time
import random
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def interpret_command_with_gpt(command):
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    prompt_parts = f"""
    Interpret the following command and provide the output in JSON format, without explaining anything:

    input: Hello, how are you?
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "I'm doing great, thank you! How can I assist you today?"
        }}
    }}

    input: Can you write a Python program to add two numbers?
    output: {{
        "action": "generate_code",
        "parameters": {{
            "task": "add two numbers",
            "code": "def add_two_numbers(num1, num2):\\n    return num1 + num2\\n\\n"
            "number1 = float(input(\\"Enter the first number: \\"))\\n"
            "number2 = float(input(\\"Enter the second number: \\"))\\n\\n"
            "result = add_two_numbers(number1, number2)\\n"
            "print(\\"The sum of\\", number1, \\" and \\\", number2, \\" is \\\", result)\\n",
            "language": "Python"
        }}
    }}

    input: What can you do?
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "I can perform tasks such as writing code, answering questions, or summarizing content!"
        }}
    }}

    input: What is the capital of Japan?
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "The capital of Japan is Tokyo."
        }}
    }}

    input: Give me a healthy recipe idea.
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "How about a spinach salad with grilled chicken and a light vinaigrette?"
        }}
    }}

    input: What's a good study tip?
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "Try the Pomodoro Technique: study for 25 minutes and take a 5-minute break."
        }}
    }}

    input: Tell me a fun fact about dinosaurs.
    output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "Did you know that some dinosaurs had feathers? They were closely related to modern birds."
        }}
    }}

    input: {command}
    output:
    """

    response = model.generate_content(prompt_parts)
    return response.text.strip().strip('`')


def process_interpreted_command(interpreted_command):
    interpreted_command = interpreted_command.strip('`')
    if interpreted_command.startswith("json"):
        interpreted_command = interpreted_command[4:].strip()

    command_data = json.loads(interpreted_command)
    action = command_data["action"]
    parameters = command_data["parameters"]

    if action == "generate_code":
        code = parameters.get("code", "")
        language = parameters.get("language", "")
        return {"code": code, "language": language}

    elif action == "general_chat":
        response = parameters.get("response", "No response provided.")
        return {"response": response}
    
    else:
        return {"error": "Unknown action"}


def write_assistant_response(response):
    with st.chat_message("assistant"):
        placeholder = st.empty()  # Placeholder for typing effect
        typed_message = ""
        # Simulate typing by adding one character at a time
        for char in response:
            typed_message += char
            placeholder.markdown(typed_message)
            time.sleep(0.03)  # Delay to simulate typing speed

    # Append the response to the session state for the chat history
    st.session_state.messages.append({"role": "assistant", "content": {"response": response}})


# Expanded list of mental health and emotional support prompts
mental_health_prompts = [
    "How are you feeling today? It's okay to share what’s on your mind.",
    "Is there anything you'd like to talk about? I'm here to listen.",
    "What’s been challenging for you lately? Your feelings are valid.",
    "How can I support you in this moment? Your well-being matters.",
    "Have you taken some time for yourself today? Self-care is important.",
    "What are some things that make you feel happy? It's good to focus on the positive.",
    "Can you name three things you’re grateful for right now? Gratitude can help us feel better.",
    "What’s something you’ve done recently that made you proud? Celebrating small wins is important.",
    "How do you usually cope when you're feeling overwhelmed? It's okay to have coping strategies.",
    "Is there a specific situation that's causing you stress? Talking about it might help.",
    "What do you enjoy doing that helps you relax? Finding joy in small things is essential.",
    "How do you take care of your mental well-being? You deserve to feel your best.",
    "Can you think of a positive memory to reflect on? Sometimes, reflecting on good times helps.",
    "What small steps can you take today to improve your mood? Every little effort counts.",
    "Are there any self-care activities you've been wanting to try? It's never too late to start.",
    "How would you like to feel right now? Acknowledging your feelings is the first step.",
    "What are some positive affirmations you can tell yourself? You are worthy and deserving of love.",
    "Is there someone you can talk to about how you're feeling? Connection is vital for healing.",
    "What’s a good way for you to express your feelings? Finding your voice is empowering.",
    "What do you wish people understood about your feelings? Communication can bring clarity.",
    "How can I help you create a safe space to talk? Your comfort is important.",
    "What techniques do you use to manage anxiety or stress? Sharing can provide new insights.",
    "How do you feel about the relationships in your life right now? Relationships impact our mental health.",
    "What are some things you could do to nurture your mental health? Small changes can make a big difference.",
    "How do you feel when you practice self-compassion? Being kind to yourself is crucial.",
    "Are there any past experiences that you’d like to talk about? Processing feelings can be healing.",
    "What’s one thing you wish you could change about your daily routine for better mental health? Small adjustments can have a big impact.",
    "Have you tried any mindfulness or relaxation techniques? These practices can help you feel more grounded.",
    "What brings you a sense of peace or comfort? Finding what soothes you is key.",
    "Are there any hobbies or activities that bring you joy? Engaging in what you love can uplift your spirits.",
    "How do you typically handle feelings of sadness or frustration? Acknowledging these feelings is the first step to managing them.",
    "What helps you to stay motivated when you’re feeling down? Finding your drive can come from within.",
    # Additional prompts for serious feelings
    "It sounds like you're going through a really tough time. I'm here to listen if you want to talk about it.",
    "I can hear that you're feeling overwhelmed. It's important to share what you're experiencing. Please talk to me.",
    "Your feelings are valid, and it's okay to express them. Have you considered reaching out to a professional for support?",
    "I'm really sorry to hear that you're feeling this way. It’s important to talk to someone who can help you.",
    "You don’t have to go through this alone. There are people who care about you and want to help.",
    # New prompt for feelings of loneliness
    "I'm really sorry to hear that you're feeling alone. Please know that I'm here for you, and you're not alone in this."
]

# In your Streamlit application logic
def main():
    st.title("AI Assistant")
    
    # Initialize session state if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").markdown(message["content"]["response"])
        else:
            st.chat_message("user").markdown(message["content"]["response"])

    # User input
    user_input = st.text_input("Your message:")
    if st.button("Send"):
        st.session_state.messages.append({"role": "user", "content": {"response": user_input}})
        
        # Check for feelings of loneliness
        if "I am alone" in user_input.lower() or "no one is there for me" in user_input.lower():
            response = "I'm really sorry to hear that you're feeling alone. Please know that I'm here for you, and you're not alone in this."
            write_assistant_response(response)
        elif any(phrase in user_input.lower() for phrase in ["suicide", "feeling depressed", "want someone", "hate", "fucked up"]):
            prompt = random.choice(mental_health_prompts)
            response = f"**It's really important to talk about how you're feeling.** {prompt}"
            write_assistant_response(response)
        else:
            # Interpret the command
            interpreted_response = interpret_command_with_gpt(user_input)
            result = process_interpreted_command(interpreted_response)
            
            if "error" in result:
                write_assistant_response(result["error"])
            else:
                if result.get("code"):
                    write_assistant_response(f"Here's your code in {result['language']}:\n```\n{result['code']}\n```")
                else:
                    write_assistant_response(result["response"])

if __name__ == "__main__":
    main()