import streamlit as st
import requests

# URL of your FastAPI server
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Chatbot")
st.title("📘 RAG Chatbot (Streamlit UI)")

# ----------------------------
# FILE UPLOAD SECTION
# ----------------------------
uploaded_file = st.file_uploader("Upload story (.docx)", type=["docx"])

if uploaded_file:
    # CHANGE: Instead of processing locally, send file to FastAPI
    files = {"file": uploaded_file.getvalue()}
    
    response = requests.post(
        f"{API_URL}/upload",
        files={"file": uploaded_file}
    )

    if response.status_code == 200:
        st.success("Story uploaded and indexed successfully!")
    else:
        st.error(f"Upload failed: {response.text}")

# ----------------------------
# CHAT SECTION
# ----------------------------
st.subheader("Chat")

user_input = st.text_input("Ask a question")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a question")
    else:
        # CHANGE: Instead of calling chat(), send request to FastAPI
        payload = {"question": user_input}
        response = requests.post(f"{API_URL}/chat", json=payload)

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.markdown(f"**Bot:** {answer}")
        else:
            st.error(f"Chat failed: {response.text}")
