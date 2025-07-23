import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def lecture_page():
    st.title("🔍 授業検索・履修登録")

    # student_id をセッションから取得
    student_id = st.session_state.get("current_student_id", None)

    if not student_id:
        st.error("❌ 学籍番号が確認されていません。先に学生情報登録画面で確認してください。")
        if st.button("🏠 ホームに戻る"):
            st.session_state.page = "学生情報登録"
            st.rerun()
        return

    # データ読み込み
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")

    lectures = lecture_sheet.get_all_records()
    students = student_sheet.get_all_records()

    df_lectures = pd.DataFrame(lectures)
    df_students = pd.DataFrame(students)

    student_row = df_students[df_students["student_id"] == student_id]
    if student_row.empty:
        st.error(f"❌ 学籍番号 {student_id} は student シートに存在しません。")
        return

    student_data = student_row.iloc[0]
    current_subjects = student_data.get("subject_name", "")
    selected_subjects = [s.strip() for s in current_subjects.split(";") if s.strip()]

    st.success(f"ようこそ、{student_data['name']} さん！現在の履修授業数: {len(selected_subjects)}")

    # 🔔 授業検索
    search_query = st.text_input("授業名 / 教員名 / 学期 / 曜日 で検索")

    if search_query:
        mask = (
            df_lectures['subject_name'].str.contains(search_query, case=False, na=False) |
            df_lectures['teacher_name1'].str.contains(search_query, case=False, na=False) |
            df_lectures['semester'].astype(str).str.contains(search_query, case=False, na=False) |
            df_lectures['day_period'].astype(str).str.contains(search_query, case=False, na=False)
        )

        results = df_lectures[mask]
        st.dataframe(results)

        if not results.empty:
            selected_subject = st.selectbox("この中から追加登録する授業を選択", results["subject_name"].unique().tolist())

            if st.button("この授業を履修登録"):
                if selected_subject in selected_subjects:
                    st.warning(f"授業「{selected_subject}」は既に登録されています。")
                else:
                    selected_subjects.append(selected_subject)
                    new_subjects = ";".join(selected_subjects)

                    idx = df_students.index[df_students["student_id"] == student_id][0]
                    df_students.at[idx, "subject_name"] = new_subjects

                    # 保存
                    student_sheet.clear()
                    student_sheet.append_row(df_students.columns.tolist())
                    for _, row in df_students.iterrows():
                        student_sheet.append_row(list(row.values))

                    st.success(f"授業「{selected_subject}」を履修登録しました ✅")
                    st.rerun()

    if st.button("🏠 ホームに戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
