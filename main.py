import streamlit as st
from student_page import student_page
from lecture_page import lecture_page
from teacher_page import teacher_page
from edit_profile import profile_edit_page
from review_page import review  # 口コミページ

# 初期化
if "page" not in st.session_state:
    st.session_state.page = "学生情報登録"

# サイドバーにメニューを表示
st.sidebar.title("メニュー")
selection = st.sidebar.radio(
    "ページを選択",
    ["学生情報登録", "プロフィール編集", "先生検索", "授業検索", "口コミ"],
    index=["学生情報登録", "プロフィール編集", "先生検索", "授業検索", "口コミ"].index(st.session_state.page)
)

# 選択変更があった場合 rerun して即反映
if selection != st.session_state.page:
    st.session_state.page = selection
    st.rerun()

# ページレンダリング
if st.session_state.page == "学生情報登録":
    student_page()
elif st.session_state.page == "プロフィール編集":
    profile_edit_page()
elif st.session_state.page == "先生検索":
    teacher_page()
elif st.session_state.page == "授業検索":
    lecture_page()
elif st.session_state.page == "口コミ":
    review()
