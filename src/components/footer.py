import streamlit as st
import base64

def footer_home():
    

    st.markdown(
        f"""
      
        <div style="margin-top:2.2rem; display: flex; gap:6px; justify-content: center; align-items: center">
            <p style="font-weight:bold; color:white">Created by ❤️Prince Kumar</p>
        </div>
        
        """,
        unsafe_allow_html=True
    )

def footer_dashboard():
    

    st.markdown(
        f"""
      
        <div style="margin-top:2rem; display: flex; gap:6px; justify-content: center; items-align: center">
            <p style="font-weight:bold; color:black">Created by ❤️Prince Kumar</p>
        </div>
        
        """,
        unsafe_allow_html=True
    )
