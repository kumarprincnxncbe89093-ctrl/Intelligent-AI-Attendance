import streamlit as st
import base64

def header_home():
    with open("logo.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <div style="display:flex;flex-direction:column; align-items:center; justify-content:center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{encoded}" width="200",height="200" style="margin-bottom: 20px;"/>
            <h1 style="test-align: center; color: #E0E3FF;"> AI Attendance <br>System</h1>
        </div>
        """,
        unsafe_allow_html=True
    )