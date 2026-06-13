import streamlit as st
import base64

def header_home():
    with open("logo.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <div class="home-hero">
            <img src="data:image/png;base64,{encoded}" class="home-logo"/>
            <h1>AI Attendance<br>System</h1>
        </div>
        <style>
            .home-hero {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin: 0.2rem 0 2.3rem;
            }}

            .home-hero .home-logo {{
                width: 108px;
                height: 108px;
                object-fit: contain;
                margin-bottom: 1rem;
                border-radius: 0.75rem;
                box-shadow: 0 14px 34px rgba(26, 32, 88, 0.16);
            }}

            .home-hero h1 {{
                text-align: center;
                color: #E0E3FF;
                text-shadow: 0 8px 20px rgba(26, 32, 88, 0.16);
            }}

            @media (max-height: 760px) {{
                .home-hero {{
                    margin-bottom: 1.5rem;
                }}

                .home-hero .home-logo {{
                    width: 92px;
                    height: 92px;
                    margin-bottom: 0.75rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def header_dashboard():
    with open("logo.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center;gap:10px;">
            <img src="data:image/png;base64,{encoded}" width="100" height="100" style="margin-bottom: 20px;"/>
            <h2 style="text-align: left; color: #5865F2;"> AI Att. <br>System</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
