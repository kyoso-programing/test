import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def student_page():
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    students = sheet.get_all_records()

    student_ids = [str(s["student_id"]) for s in students if "student_id" in s]

    if "student_registered" not in st.session_state:
        # まだセッション変数がない場合、登録状況から初期化
        st.session_state.student_registered = len(students) > 0

    if not st.session_state.student_registered:
        st.title("🎓 学生情報登録（初回のみ）")

        with st.form("student_register_form"):
            student_id = st.text_input("学籍番号")
            name = st.text_input("名前")
            submitted = st.form_submit_button("登録する")

            if submitted:
                if not student_id or not name:
                    st.warning("学籍番号と名前は必須です。")
                elif student_id in student_ids:
                    st.error(f"学籍番号 {student_id} は既に登録されています。")
                else:
                    # 最小限で登録（詳細は後から編集）
                    new_row = [student_id, name, "", 0, 0]
                    try:
                        sheet.append_row(new_row)
                        st.success(f"{name} さんを登録しました ✅")
                        st.session_state.student_registered = True
                        st.experimental_rerun()  # 登録後に画面を更新
                    except Exception as e:
                        st.error("スプレッドシートへの保存に失敗しました。")
                        st.exception(e)
    else:
        st.title("✅ 登録済み")

        st.info("学生情報が登録済みです。以下の操作を選んでください。")

        col1, col2, col3 = st.columns(3)

        if col1.button("プロフィール編集"):
            st.session_state.page = "プロフィール編集"

        if col2.button("先生検索"):
            st.session_state.page = "先生検索"

        if col3.button("授業検索"):
            st.session_state.page = "授業検索"
