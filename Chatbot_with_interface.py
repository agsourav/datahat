#in terminal: pip install streamlit
import streamlit as st
from transformers import pipeline, Conversation
import time

#A chatbot requires 3 things
# 1. Interactive panel to accept user input
# 2. A model to process user input (LLM)
# 3. A conversation buffer to maintain the history

about_us = st.sidebar.subheader("About Us")
detail = st.sidebar.text("""Datahat simplifies AI
Our vision is to help you succeed
in your career in AI""")

device = st.sidebar.selectbox("Select CPU/GPU", ("cpu","cuda"))
audio_out = st.sidebar.selectbox("Get audio output?", ("yes", "no"))

about_this_bot = st.sidebar.caption("This is a _demo chatbot_.")
chat_llm = pipeline(task="conversational", model="facebook/blenderbot-400M-distill", device=device)

if audio_out=="yes":
    audio_llm = pipeline(task="text-to-speech", model="facebook/mms-tts-eng", device=device)

system_prompt = """You are a helpful AI chatbot that responds in friendly manner"""

chat_history = Conversation([{"role":"system", "content":system_prompt}])

#creating chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt := st.chat_input("type your prompt here..."):
    with st.chat_message("user"):
    #user.write(prompt)
        st.markdown(prompt)
        user_chat = {"role": "user", "content": prompt}
        chat_history.add_message(user_chat)
        st.session_state.messages.append(user_chat)
    try:
        response = chat_llm(chat_history, max_length=1024)
    except:
        error_message = "You exceeded the maximum token limitation for the model!!"
        with st.chat_message("assistant"):
            st.markdown(error_message)
        exit()

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = response.messages[-1]["content"]
        if audio_out=="yes":
            audio_response = audio_llm(assistant_response)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.1)

            message_placeholder.markdown(full_response + "| ")
        message_placeholder.markdown(full_response)
        if audio_out=="yes":
            st.audio(audio_response["audio"], sample_rate=audio_response["sampling_rate"])
        st.session_state.messages.append({"role":"assistant", "content":response.messages[-1]["content"]})

