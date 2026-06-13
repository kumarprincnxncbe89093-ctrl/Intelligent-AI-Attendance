import streamlit as st
from PIL import Image
import hashlib


def _image_from_upload(file):
    image = Image.open(file)
    image.load()
    return image.convert("RGB").copy()


def _file_signature(file):
    value = file.getvalue()
    return hashlib.sha256(value).hexdigest()


@st.dialog("Capture or upload photos")
def add_photo_dialog():
    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
      st.session_state.photo_tab='camera'

    t1,t2=st.columns(2)

    with t1:
        type_camera='primary' if st.session_state.photo_tab=='camera' else 'tertiary'
        if st.button("Camera",type=type_camera,width='stretch'):
           st.session_state.photo_tab='camera'
    
    with t2:
        type_upload='primary' if st.session_state.photo_tab=='upload' else 'tertiary'
        if st.button("Upload photos",type=type_upload,width='stretch'):
           st.session_state.photo_tab='upload'

    
    if st.session_state.photo_tab=='camera':
        cam_photo=st.camera_input('Take Snapshot',key='dialog_cam')

        if cam_photo:
          signature = _file_signature(cam_photo)
          if st.session_state.get('last_camera_photo') != signature:
            st.session_state.attendance_images.append(_image_from_upload(cam_photo))
            st.session_state.last_camera_photo = signature
            st.toast('Photo Captured')
            st.rerun()

    if st.session_state.photo_tab=='upload':
        uploaded_files=st.file_uploader('Choose image files',type=['jpg','png','jpeg'],accept_multiple_files=True,key='dialog_upload')

        if uploaded_files:
            processed_uploads=st.session_state.setdefault('processed_attendance_uploads',set())
            new_count=0
            for f in uploaded_files:
                signature=_file_signature(f)
                if signature in processed_uploads:
                    continue
                st.session_state.attendance_images.append(_image_from_upload(f))
                processed_uploads.add(signature)
                new_count+=1

            if new_count:
                st.toast(f'{new_count} Photo Uploaded Successfully')
                st.rerun()

    st.divider()
    if st.button('Done',type='primary',width='stretch'):
       st.rerun()




   
