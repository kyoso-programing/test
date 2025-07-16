import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def teacher_page():
    st.title("👨‍🏫 先生検索")

    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("teacher")
    teachers = sheet.get_all_records()
    df = pd.DataFrame(teachers)

    search_name = st.text_input("先生の名前で検索")
    if search_name:
        results = df[df['teacher_name'].str.contains(search_name, case=False, na=False)]
        st.dataframe(results)
    else:
        st.dataframe(df)

    # 🔔 遷移ボタン
    if st.button("🏠 ホーム（学生ページ）に戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
