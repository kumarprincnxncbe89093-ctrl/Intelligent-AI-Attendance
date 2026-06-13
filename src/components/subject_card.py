import streamlit as st
from html import escape

def subject_card(name,code,section,stats=None,footer_callback=None):
    safe_name = escape(str(name))
    safe_code = escape(str(code))
    safe_section = escape(str(section))

    html=f"""
        <div style="background:white; border-left:8px solid #EB459E; padding:25px;border-radius:20px;border:1px solid black; margin-bottom: 20px;;">
        <h3 style="margin:0; color: #1e293b; font-size:1.5rem">{safe_name}</h3>
        <p style="color: #64748b; margin:10px 0;">Code : <span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px;">{safe_code}</span> | Section : {safe_section}</p>
        """
    if stats:
        html+="""
        <div style="display:flex;gap:8px;flex-wrap:wrap;">

        """
        for icon,label,value in stats:
            html+=f'<div style="background: #EB459E10; padding:5px 12px; border-radius:12px;font-size:0.9rem">{escape(str(icon))}<b>{escape(str(value))}</b> {escape(str(label))} </div>'

            

        html+="</div>"

    st.markdown(html,unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
