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

            @media (max-width: 760px) {{
                .home-hero {{
                    margin: 0.15rem 0 1.4rem;
                }}

                .home-hero .home-logo {{
                    width: 82px;
                    height: 82px;
                    margin-bottom: 0.7rem;
                }}

                .home-hero h1 {{
                    font-family: 'Outfit', sans-serif !important;
                    font-size: 2rem !important;
                    line-height: 1.08 !important;
                    color: #ffffff !important;
                    letter-spacing: 0 !important;
                    text-shadow: 0 6px 16px rgba(26, 32, 88, 0.18);
                }}
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
        <div class="dashboard-brand">
            <img src="data:image/png;base64,{encoded}" class="dashboard-logo"/>
            <h2> AI Att. <br>System</h2>
        </div>
        <style>
            .dashboard-brand {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }}

            .dashboard-logo {{
                width: 100px;
                height: 100px;
                object-fit: contain;
                margin-bottom: 20px;
            }}

            .dashboard-brand h2 {{
                text-align: left;
                color: #5865F2 !important;
            }}

            @media (max-width: 760px) {{
                .dashboard-brand {{
                    justify-content: flex-start;
                    gap: 8px;
                }}

                .dashboard-logo {{
                    width: 72px;
                    height: 72px;
                    margin-bottom: 10px;
                }}

                .dashboard-brand h2 {{
                    font-family: 'Outfit', sans-serif !important;
                    font-size: 1.45rem !important;
                    line-height: 1.05 !important;
                    color: #5865F2 !important;
                    letter-spacing: 0 !important;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
