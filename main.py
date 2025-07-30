# main.py
import streamlit as st
import pandas as pd
from auth import get_gspread_client, SPREADSHEET_ID
from student_page import student_page
from lecture_page import lecture_page
from teacher_page import teacher_page
from edit_profile import profile_edit_page
from review_page import review_page

# 🔑 認証
client = get_gspread_client()
try:
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet_names = [ws.title for ws in spreadsheet.worksheets()]
    st.write("📄 利用可能なシート一覧:", sheet_names)
except Exception as e:
    st.error(f"❌ シート一覧の取得に失敗しました: {e}")
# 初期化
if "page" not in st.session_state:
    st.session_state.page = "学生情報登録"

# サイドバー
st.sidebar.title("メニュー")
selection = st.sidebar.radio(
    "ページを選択",
    ["学生情報登録", "プロフィール編集", "先生検索", "授業検索", "口コミ"],  # ← 追加
    index=["学生情報登録", "プロフィール編集", "先生検索", "授業検索", "口コミ"].index(st.session_state.page)
)

# ページ変更時の再実行
if selection != st.session_state.page:
    st.session_state.page = selection
    st.rerun()

# ページ表示
if st.session_state.page == "学生情報登録":
    student_page(client, SPREADSHEET_ID)

elif st.session_state.page == "プロフィール編集":
    if "student_id" not in st.session_state:
        st.warning("⚠️ 学生IDが未登録です。まず「学生情報登録」で登録してください。")
    else:
        # シートからデータ取得
        lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
        student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
        df_lectures = pd.DataFrame(lecture_sheet.get_all_records())
        df_students = pd.DataFrame(student_sheet.get_all_records())

        profile_edit_page(df_lectures, df_students, student_sheet, st.session_state.student_id)

elif st.session_state.page == "先生検索":
    teacher_page(client, SPREADSHEET_ID)

elif st.session_state.page == "授業検索":
    lecture_page(client, SPREADSHEET_ID)

elif st.session_state.page == "口コミ":
    review_page(client, SPREADSHEET_ID)
