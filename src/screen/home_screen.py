import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from pathlib import Path
from src.components.footer import footer_home
BASE_DIR = Path.cwd()   # Project root


def home_screen():
    student_logo = BASE_DIR / "student.png"
    teacher_logo = BASE_DIR / "teacher.png"

    header_home()
    style_background_home()
    style_base_layout()
    col1,col2 =st.columns(2,gap="large")
    with col1:
        st.header("I'm Student")
        st.image(str(student_logo), width=140)
        if st.button("Student Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
            st.session_state["login_type"]="student"
            st.rerun()
    with col2:
        st.header("I'm Teacher")
        st.image(str(teacher_logo), width=140)
        if st.button("Teacher Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
            st.session_state["login_type"]="teacher"
            st.rerun()
    footer_home()