import streamlit as st
import requests

st.title("Streamlit Dashboard")

API_URL = "http://127.0.0.1:5000/"

uname=st.text_input('username')
st.write("djd")
if st.button('click'):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            st.success("API Connected")
            st.write("Username:", data["username"])
            st.write("Role:", data["role"])

        else:
            st.error("API Error")

    except requests.exceptions.ConnectionError:
        st.error("Flask API is not running")
