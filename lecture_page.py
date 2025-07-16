import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def lecture_page():
    st.title("🔍 授業検索")

    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    lectures = sheet.get_all_records()
    df = pd.DataFrame(lectures)

    search_title = st.text_input("授業名で検索")
    if search_title:
        results = df[df['subject_name'].str.contains(search_title, case=False, na=False)]
        st.dataframe(results)
    else:
        st.dataframe(df)

    # 🔔 遷移ボタン
    if st.button("🏠 ホーム（学生ページ）に戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
