import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Calculator Agent", page_icon="🧮")
st.title("AI Calculator Agent")

query = st.text_input("Ask me:")

if st.button("Calculate") and query:
    with st.spinner("Thinking..."):
        st.success(run_agent(query))
