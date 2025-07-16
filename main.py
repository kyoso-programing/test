import streamlit as st
from student_page import student_page
from lecture_page import lecture_page
from teacher_page import teacher_page
from edit_profile import profile_edit_page

if "page" not in st.session_state:
    st.session_state.page = "学生情報登録"

if st.session_state.page == "学生情報登録":
    student_page()
elif st.session_state.page == "プロフィール編集":
    profile_edit_page()
elif st.session_state.page == "先生検索":
    teacher_page()
elif st.session_state.page == "授業検索":
    lecture_page()
