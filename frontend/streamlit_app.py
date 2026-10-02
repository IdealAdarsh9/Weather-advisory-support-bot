from __future__ import annotations

import uuid
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from app.graph import invoke

st.set_page_config(page_title="Weather-Advisory Support Bot", page_icon="🌦️", layout="centered")

st.title("Weather-Advisory Support Bot")
st.caption("Live Open-Meteo weather + controlled safety SOPs")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Session")
    if st.button("Start new session"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    st.markdown("**Policy model:** deterministic SOP matching")
    st.markdown("**Weather:** Open-Meteo")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("meta"):
            with st.expander("Trace / policy basis"):
                st.code(message["meta"])

prompt = st.chat_input("Ask about outdoor activity safety, e.g. 'Is it safe to cycle in Bhopal today?'")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking live weather and safety policies..."):
            try:
                result = invoke(prompt, st.session_state.thread_id)
                answer = result.get("response") or "I couldn't produce a response safely."
                trace = "\n".join(result.get("trace", []))
            except Exception as exc:
                answer = "I couldn't answer safely because a required system step failed. Please try again shortly."
                trace = f"Unhandled application error: {type(exc).__name__}: {exc}"
        st.markdown(answer)
        with st.expander("Trace / policy basis"):
            st.code(trace or "No trace available.")

    st.session_state.messages.append({"role": "assistant", "content": answer, "meta": trace})
