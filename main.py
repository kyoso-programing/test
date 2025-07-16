import streamlit as st
from student_page import student_page
from lecture_page import lecture_page
from teacher_page import teacher_page

st.sidebar.title("メニュー")
page = st.sidebar.selectbox("ページを選択", ["学生情報登録", "授業検索", "先生検索"])

if page == "学生情報登録":
    student_page()
elif page == "授業検索":
    lecture_page()
elif page == "先生検索":
    teacher_page()
