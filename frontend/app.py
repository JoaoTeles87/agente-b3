import streamlit as st
import requests

st.title("B3 AI Agent")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    response = requests.get(f"http://localhost:8000/?query={query}")
    st.write(response.json())
