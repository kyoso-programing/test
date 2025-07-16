import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def student_page():
    st.title("🎓 学生情報登録")
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    students = sheet.get_all_records()

    student_ids = [str(s["student_id"]) for s in students if "student_id" in s]

    if students:
        st.info("✅ 学生情報はすでに登録されています。追加する場合は重複しない学籍番号で登録してください。")

    with st.form("student_form"):
        student_id = st.text_input("学籍番号")
        name = st.text_input("名前")
        interests_input = st.text_input("興味分野（カンマ区切り）", placeholder="例：物理学,AI,留学")
        total_required_credits = st.number_input("必要単位数", min_value=0, value=124)
        earned_credits = st.number_input("取得済み単位数", min_value=0, value=0)

        submitted = st.form_submit_button("追加する")

        if submitted:
            if not student_id or not name:
                st.warning("学籍番号と名前は必須です。")
            elif student_id in student_ids:
                st.error(f"学籍番号 {student_id} は既に登録されています。")
            else:
                interests = ";".join([s.strip() for s in interests_input.split(",")])
                new_row = [student_id, name, interests, total_required_credits, earned_credits]
                try:
                    sheet.append_row(new_row)
                    st.success(f"{name} さんの情報を追加しました ✅")
                except Exception as e:
                    st.error("スプレッドシートへの保存に失敗しました。")
                    st.exception(e)
