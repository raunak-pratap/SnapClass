import streamlit as st 
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home, style_background_dashboard

def home_screen():
    
    header_home()
    style_background_dashboard()
    style_background_home()
    style_base_layout()
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <h1 style="
            color:#272a33;
            font-size:43px;
            font-family:'Climate Crisis', sans-serif;
            line-height:0.85;
            ">
            I'm<br>Student
            </h1>
            """, unsafe_allow_html=True)

        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Student Portal", type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()
    with col2:
        st.markdown("""
            <h1 style="
            color:#272a33;
            font-size:43px;
            font-family:'Climate Crisis', sans-serif;
            line-height:0.85;
            ">
            I'm<br>Teacher
            </h1>
            """, unsafe_allow_html=True)
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button("Teacher Portal", type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()  # Rerun the app to reflect the change in login_type

    footer_home()