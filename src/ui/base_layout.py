import streamlit as st

def style_background_home():

    st.markdown("""
        <style>
                .stApp {
                    background:#5865f2 !important;
                }

                .block-container {
                    max-width: 1060px !important;
                    padding-top: 1rem !important;
                    padding-bottom: 1rem !important;
                }

                .stApp div[data-testid="stHorizontalBlock"] {
                    align-items: stretch;
                    gap: 2.4rem;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:white !important;
                    padding:2rem 2.3rem !important;
                    border-radius:2.2rem !important;
                    min-height: 245px;
                    box-shadow: 0 18px 45px rgba(26, 32, 88, 0.14);
                    border: 1px solid rgba(255,255,255,0.65);
                    transition: transform 0.25s ease, box-shadow 0.25s ease;
                }

                .stApp div[data-testid="stColumn"]:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 22px 55px rgba(26, 32, 88, 0.20);
                }

                .stApp div[data-testid="stColumn"] h2 {
                    color: #2d3040 !important;
                    font-size: 1.85rem !important;
                    margin-bottom: 0.8rem !important;
                }

                .stApp div[data-testid="stColumn"] img {
                    margin: 0.2rem 0 1.2rem 0;
                    filter: drop-shadow(0 14px 18px rgba(88, 101, 242, 0.12));
                }

                .stApp div[data-testid="stColumn"] button {
                    margin-top: 0.25rem;
                    min-width: 150px;
                    box-shadow: 0 10px 22px rgba(88, 101, 242, 0.24);
                }

                @media (max-width: 760px) {
                    .block-container {
                        padding-left: 1rem !important;
                        padding-right: 1rem !important;
                    }

                    .stApp div[data-testid="stHorizontalBlock"] {
                        gap: 1rem;
                    }

                    .stApp div[data-testid="stColumn"] {
                        padding: 1.4rem 1.5rem !important;
                        min-height: 215px;
                        border-radius: 1.7rem !important;
                    }
                }

        </style>
                """,unsafe_allow_html=True)

def style_background_dashboard():

    st.markdown("""
        <style>
                .stApp {
                    background: #E0E3FF !important;
                }

        </style>
                """,unsafe_allow_html=True)

def style_base_layout():

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            /* Hide Top Bar of streamlit */
                #MainMenu, footer, header {
                    visibility: hidden;
                }

                .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 1.5rem;
                    max-width: 980px;
                }

                h1 {
                    font-family: 'Climate Crisis', sans-serif !important;
                    font-size: 2.4rem !important;
                    line-height: 1.1 !important;
                    margin-bottom: 0 !important;
                    
                }
                h2 {
                    font-family: 'Climate Crisis', sans-serif !important;
                    font-size: 2rem !important;
                    line-height: 1.1 !important;
                    margin-bottom: 0.rem !important;
                }

                h3,h4,p{
                    font-family: 'Outfit', sans-serif ;

                }
                button,
                button[data-testid="stBaseButton-primary"] {
                    border-radius: 1.5rem !important;
                    background-color: #5865F2 !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    }
                button *,
                button[data-testid="stBaseButton-primary"] * {
                    color: white !important;
                    }
                button[kind="secondary"],
                button[data-testid="stBaseButton-secondary"] {
                    border-radius: 1.5rem !important;
                    background-color: #EB458E !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    }
                button[kind="tertiary"],
                button[data-testid="stBaseButton-tertiary"] {
                    border-radius: 1.5rem !important;
                    background-color: black !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    }
                button[kind="tertiary"] *,
                button[data-testid="stBaseButton-tertiary"] * {
                    color: white !important;
                    }
                button:hover {
                    transform: scale(1.05) !important;
                    }
        </style>
                """,unsafe_allow_html=True)
