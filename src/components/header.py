import streamlit as st

import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        </style>
        
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;">
            <img src="{logo_url}" style="height:160px;" />
            <h1 style="text-align:center; color:#272a33; font-family: 'Climate Crisis', sans-serif; font-weight: 400;">
                SNAP<br/>CLASS
            </h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:20px;">
            <img src="{logo_url}" style="height:90px;" />
            <div style="
                font-family:'Climate Crisis', sans-serif;
                font-size:42px;
                line-height:0.85;
                color:#5865F2;
            ">
                SNAP<br>CLASS
            </div>
        </div>
    """, unsafe_allow_html=True)

