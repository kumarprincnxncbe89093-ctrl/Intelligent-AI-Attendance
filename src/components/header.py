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

def header_dashboard():
    with open("logo.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center;gap:10px;">
            <img src="data:image/png;base64,{encoded}" width="100",height="100" style="margin-bottom: 20px;"/>
            <h2 style="text-align: left; color: #5865F2;"> AI Att. <br>System</h2>
        </div>
        """,
        unsafe_allow_html=True
    )