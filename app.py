
import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from src.agent import run_agent, conversation_history


st.set_page_config(
    page_title="Academic Support Agent",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Academic Support Agent")
st.caption("Ask questions about courses, policies, grades, and deadlines.")

st.info(
    "This assistant uses fictional sample academy data. "
    "Verify important academic information with your instructor."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your academic question...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_agent(prompt)
            except Exception as error:
                response = (
                    f"Something went wrong: "
                    f"{type(error).__name__}: {error}"
                )

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
