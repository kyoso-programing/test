import streamlit as st
from auth import get_gspread_client
from student_page import student_page
from edit_profile import profile_edit_page
from teacher_page import teacher_page
from lecture_page import lecture_page
from review_page import review_page

# Google Sheets 認証
client = get_gspread_client()
SPREADSHEET_ID = "1ia3ljvxeVCgZo5gXryN96yHHlDwlv6THmLDmM8UiI1U"

# 初期セッション状態の設定
if "page" not in st.session_state:
    st.session_state.page = "学生情報登録"
if "student_id" not in st.session_state:
    st.session_state.student_id = None

# ページ選択ロジック
page = st.session_state.page

if page == "学生情報登録":
    student_page(client, SPREADSHEET_ID)
elif page == "プロフィール編集":
    from gspread_dataframe import get_as_dataframe
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    df_students = get_as_dataframe(student_sheet).dropna(how="all")
    df_lectures = get_as_dataframe(lecture_sheet).dropna(how="all")
    profile_edit_page(df_lectures, df_students, student_sheet, st.session_state.student_id)
elif page == "先生検索":
    teacher_page(client, SPREADSHEET_ID)
elif page == "授業検索":
    lecture_page(client, SPREADSHEET_ID)
elif page == "口コミ":
    review_page(client, SPREADSHEET_ID)
