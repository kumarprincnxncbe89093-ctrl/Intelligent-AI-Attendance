import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipeline.face_pipeline import predict_attendence,get_face_embeddings,train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject,update_student_biometrics,DatabaseConnectionError
import time
from src.components.subject_card import subject_card

from src.components.dialog_enroll import enroll_dialog

def render_student_biometric_updates(student_id):
    st.subheader("Update Profile")
    c1,c2=st.columns(2,gap="medium")

    with c1:
        if st.button(
            "Update Face ID",
            type="secondary",
            width="stretch",
            icon=":material/face:",
            key="open_update_face",
        ):
            st.session_state.show_update_face=True
            st.session_state.show_update_voice=False

    with c2:
        if st.button(
            "Update Voice ID",
            type="secondary",
            width="stretch",
            icon=":material/mic:",
            key="open_update_voice",
        ):
            st.session_state.show_update_voice=True
            st.session_state.show_update_face=False

    if st.session_state.get("show_update_face"):
        with st.container(border=True):
            title_col, close_col=st.columns([3,1],vertical_alignment="center")
            with title_col:
                st.subheader("Update Face ID")
            with close_col:
                if st.button(
                    "Close",
                    type="tertiary",
                    width="stretch",
                    icon=":material/close:",
                    key="close_update_face",
                ):
                    st.session_state.show_update_face=False
                    st.rerun()

            photo_source=st.camera_input(
                "Capture your new face photo",
                width=700,
                key="update_face_photo",
            )

            if st.button(
                "Save Face ID",
                type="primary",
                width="stretch",
                disabled=photo_source is None,
                key="save_update_face",
            ):
                with st.spinner("Updating Face ID..."):
                    img=np.array(Image.open(photo_source))
                    encodings=get_face_embeddings(img)

                    if not encodings:
                        st.error("Could not detect a face. Please capture a clear front-facing photo.")
                        return

                    try:
                        updated=update_student_biometrics(
                            student_id,
                            face_embedding=encodings[0].tolist(),
                        )
                    except DatabaseConnectionError as exc:
                        st.error(str(exc))
                        return

                    if not updated:
                        st.error("Face ID was not updated. Please try again.")
                        return

                    st.session_state.student_data.update(updated[0])

                    train_classifier()
                    st.session_state.show_update_face=False
                    st.success("Face ID updated successfully.")
                    time.sleep(1)
                    st.rerun()

    if st.session_state.get("show_update_voice"):
        with st.container(border=True):
            title_col, close_col=st.columns([3,1],vertical_alignment="center")
            with title_col:
                st.subheader("Update Voice ID")
            with close_col:
                if st.button(
                    "Close",
                    type="tertiary",
                    width="stretch",
                    icon=":material/close:",
                    key="close_update_voice",
                ):
                    st.session_state.show_update_voice=False
                    st.rerun()

            try:
                audio_data=st.audio_input(
                    "Record a short phrase like I am present",
                    key="update_voice_audio",
                )
            except Exception:
                audio_data=None
                st.error("Audio recorder failed to load.")

            if st.button(
                "Save Voice ID",
                type="primary",
                width="stretch",
                disabled=audio_data is None,
                key="save_update_voice",
            ):
                with st.spinner("Updating Voice ID..."):
                    voice_embedding=get_voice_embedding(audio_data.read())

                    if not voice_embedding:
                        st.error("Could not create a voice profile. Please record again.")
                        return

                    try:
                        updated=update_student_biometrics(
                            student_id,
                            voice_embedding=voice_embedding,
                        )
                    except DatabaseConnectionError as exc:
                        st.error(str(exc))
                        return

                    if not updated:
                        st.error("Voice ID was not updated. Please try again.")
                        return

                    st.session_state.student_data.update(updated[0])

                    st.session_state.show_update_voice=False
                    st.success("Voice ID updated successfully.")
                    time.sleep(1)
                    st.rerun()

def student_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    
    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {student_data["name"]}""")
        if st.button("Logout", type="secondary", key="loginbackbtn3"):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.rerun()

    st.space()
    render_student_biometric_updates(student_id)
    st.divider()

    c1,c2=st.columns(2)
    with c1:
        st.header("You Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject",type="primary",width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        try:
            subjects=get_student_subjects(student_id)
            logs=get_student_attendance(student_id)
        except DatabaseConnectionError as exc:
            st.error(str(exc))
            footer_dashboard()
            return

    stats_map={}

    for log in logs:
        sid=log['subject_id']

        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}

        stats_map[sid]['total']+=1

        if log.get('is_present'):
            stats_map[sid]['attended']+=1
    
    cols=st.columns(2)
    visible_subjects = [node["subjects"] for node in subjects if node.get("subjects")]

    if not visible_subjects:
        st.info("You are not enrolled in any subjects yet.")

    for i,sub in enumerate(visible_subjects):
        sid=sub['subject_id']


        stats=stats_map.get(sid,{"total":0,"attended":0})

        def unenroll_button(subject_id=sid, subject_name=sub['name']):
            if st.button(
                "Unenroll from this course",
                type='tertiary',
                width='stretch',
                key=f"unenroll_{subject_id}",
            ):
                try:
                    unenroll_student_to_subject(student_id,subject_id)
                except DatabaseConnectionError as exc:
                    st.error(str(exc))
                    return
                st.toast(f"Unenrolled from {subject_name}")
                time.sleep(1)
                st.rerun()
        

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('🗓️','Total',stats['total']),
                    ('✅','Attended',stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go Back to Home",
            type="secondary",
            key="loginbackbtn3",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    
    st.header("Login using FaceID",text_alignment="center")
    st.space()
    st.space()
    
    show_registration=False
    
    photo_source=st.camera_input("Position your face in the center",width=700)

    if photo_source:
        img= np.array(Image.open(photo_source))
        with st.spinner("AI is scanning..."):
            detected,all_ids,num_faces=predict_attendence(img)

            if num_faces==0:
                st.warning("Face not found!")

            if num_faces>1:
                st.warning("Multiple faces found!!")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    try:
                        all_students=get_all_students()
                    except DatabaseConnectionError as exc:
                        st.error(str(exc))
                        return

                    student=next((s for s in all_students if str(s["student_id"])==str(student_id)),None)

                    if student:
                        if "user" not in st.session_state:
                            st.session_state.user = {"role": None}
                        if "is_logged_in" not in st.session_state:
                            st.session_state.is_logged_in = False
                        st.session_state.is_logged_in = True
                        st.session_state.user["role"] = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                
                else:
                    st.info("Face not recognized. You might be a new student.")
                    show_registration=True

    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name=st.text_input("Enter your name",placeholder="E.g. prince kumar")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll your voice for voice-only attendance")

            audio_data=None

            try:
                audio_data=st.audio_input("Record a short phrase like I am present, My name is ... ")
            except Exception:
                st.error("Audio Data Failed!!")


            if st.button("Create Account",type="primary"):
                if new_name:
                    with st.spinner("Creating profile"):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())

                            try:
                                response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            except DatabaseConnectionError as exc:
                                st.error(str(exc))
                                return

                            if response_data:
                                train_classifier()

                                st.session_state.is_logged_in=True
                                if "user" not in st.session_state:
                                    st.session_state.user = {"role": None}
                                st.session_state.user["role"] = "student"
                                st.session_state.student_data=response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Could not capture your facial features for registration")

                else:
                    st.warning("Please enter your name!!")



    footer_dashboard()
