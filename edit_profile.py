import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def profile_edit_page():
    st.title("📝 プロフィール編集")

    # スプレッドシートからデータ取得
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")

    students = student_sheet.get_all_records()
    lectures = lecture_sheet.get_all_records()

    df_students = pd.DataFrame(students)
    df_lectures = pd.DataFrame(lectures)

    student_id = st.text_input("編集する学籍番号")

    if student_id:
        student_row = df_students[df_students["student_id"] == student_id]

        if not student_row.empty:
            current = student_row.iloc[0]

            st.subheader("プロフィール情報編集")
            with st.form("edit_profile_form"):
                interests_input = st.text_input(
                    "興味分野（カンマ区切り）", 
                    value=current.get("interests", "")
                )
                submitted = st.form_submit_button("更新する")

                if submitted:
                    idx = df_students.index[df_students["student_id"] == student_id][0]
                    df_students.at[idx, "interests"] = interests_input

                    # 保存
                    student_sheet.clear()
                    student_sheet.append_row(["student_id", "name", "interests", "total_required_credits", "earned_credits"])
                    for _, row in df_students.iterrows():
                        student_sheet.append_row(list(row.values))

                    st.success(f"学籍番号 {student_id} のプロフィールを更新しました ✅")

            # 🔔 自分が選んだ授業を管理
            st.subheader("履修授業管理")

            selected_subjects = st.multiselect(
                "履修する授業を選択", 
                options=df_lectures["subject_name"].unique()
            )

            if selected_subjects:
                selected_lectures = df_lectures[df_lectures["subject_name"].isin(selected_subjects)]

                total_credits = selected_lectures["class_credit"].sum()
                st.info(f"✅ 現在の総単位数: {total_credits} 単位")

                st.subheader("時間割プレビュー")
                st.dataframe(
                    selected_lectures[["subject_name", "semester", "day", "period", "place"]]
                )
            else:
                st.write("履修授業が未選択です。")

        else:
            st.warning(f"学籍番号 {student_id} は見つかりません。")

    # 戻るボタン
    if st.button("🏠 ホーム（学生ページ）に戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
