import streamlit as st
import requests
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(page_title="ChatBot MQ", layout="wide", page_icon="🤖")

# Sidebar menu
with st.sidebar:
    st.markdown("### 😎 Minh Quý\n### 🤖 Multiple ChatBot")
    endpoint = option_menu('',
                           ['Chat', 'Vision'],
                           icons=['chat-dots', 'camera'],
                           default_index=0)

# Chat Endpoint
if endpoint == "Chat":
    st.header("Chat :speech_balloon:")
    input = st.text_input("Input your question:", key="qa_input")
    submit = st.button("Ask the question")
    
    if submit:
        response = requests.post("http://fastapi_app:8000/chat/", json={"question": input})
        if response.status_code == 200:
            st.subheader("The Response is")
            st.write(response.json()['response'])
        else:
            st.error("Failed to get response")

# Vision Endpoint
elif endpoint == "Vision":
    st.header("Vision :camera:")
    input = st.text_input("Input your text (optional):", key="vision_input")
    image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"], key="vision_image")
    submit = st.button("Analyze image")
    
    if submit and image:
        files = {"image": image.getvalue()}
        data = {"input": input}
        response = requests.post("http://fastapi_app:8000/vision/", data=data, files=files)
        if response.status_code == 200:
            st.subheader("The Response is")
            st.write(response.json()['response'])
        else:
            st.error("Failed to get response")
    elif submit:
        st.error("Please upload an image")