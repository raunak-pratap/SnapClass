import streamlit as st 
from PIL import Image
import numpy as np
import time 

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding, identify_speaker
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():

    if "student_data" not in st.session_state:
        st.session_state.is_logged_in = False
        st.warning("Session expired. Please login again.")
        st.stop()

    student_data = st.session_state.student_data

    # DEBUG
    st.write("student_data =", student_data)
    st.write("type =", type(student_data))

    if not student_data:
        st.error("Student information not found.")
        st.stop()

    if isinstance(student_data, list):
        st.error("student_data is a list")
        st.stop()

    if "student_id" not in student_data:
        st.error("student_id key missing")
        st.write(student_data)
        st.stop()

    student_id = student_data["student_id"]

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state :
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()



    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()

    show_registration = False

    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning.."):
            detected, all_ids, num_faces = predict_attendance(img)

        if num_faces == 0:
            st.warning("Face not detected. Please try again.")
        elif num_faces > 1:
            st.warning("Multiple faces detected. Please ensure only your face is visible.")
        else:
            if detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()

                student = next(
                    (s for s in all_students if s["student_id"] == student_id),
                    None
                )

                if student is None:
                    st.error("Student record not found in the database.")
                    st.stop()

                st.session_state.is_logged_in = True
                st.session_state.user_role = "student"
                st.session_state.student_data = student

                st.toast(f"Welcome Back, {student['name']}!")
                time.sleep(1)
                st.rerun()

            else:
                st.info("Face not recognized. Please ensure you are registered in the system.")
                show_registration = True 

    if show_registration:
        st.space()
        st.header("Register your face to access the system", text_alignment='center')
        new_name = st.text_input("Enter your name", placeholder="Raunak Pratap")

        st.subheader("Optional: Voice Enrollment")
        st.info("Enroll your for voice only attendance")

        audio_data = None

        try:
            audio_data = st.audio_input("Record your voice")
        except Exception as e:
            st.error("Audio Data failed")

        if st.button('Create Account', type='primary'):
            if new_name:
                with st.spinner("Creating Profile..."):
                    img = np.array(Image.open(photo_source))
                    embedding = get_face_embeddings(img)
                    if embedding:
                        face_emb = embedding[0].tolist()

                        voice_emb = None
                        if audio_data:
                            voice_emb = get_voice_embedding(audio_data.read())

                        response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb)


                        if response_data:
                            train_classifier()
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data
                            st.toast(f"Welcome, {new_name}! Your profile has been created.")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("Couldn't capture your facial features for registration")

            else:
                st.warning("Please enter your name ")


    footer_dashboard()