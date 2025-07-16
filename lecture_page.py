import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

LECTURE_HEADERS = [
    "class_id", "subject_name", "class_name",
    "teacher_name1", "teacher_name2", "teacher_name3", "teacher_name4",
    "class_category", "semester", "day", "period", "keyword", "place", "language",
    "class_satisfaction", "class_difficulty", "textbook", "test_report",
    "test_bringingin", "test_times", "test_difficulty", "comments",
    "course_requirements", "attendance", "evaluation_criteria",
    "class_credit", "student_number", "class_style"
]

def lecture_page():
    st.title("🔍 授業検索")
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
        lectures = sheet.get_all_records(expected_headers=LECTURE_HEADERS)
        df = pd.DataFrame(lectures)

        search_title = st.text_input("授業名で検索")
        if search_title:
            results = df[df['subject_name'].str.contains(search_title, case=False, na=False)]
            st.dataframe(results)

            if results.empty:
                st.info("該当する授業が見つかりません。新しく追加できます。")

                with st.form("add_lecture_form"):
                    new_subject_name = st.text_input("新しい授業名", value=search_title)
                    new_teacher_name = st.text_input("担当教員名")
                    semester = st.text_input("学期（例：2025春）")
                    submitted = st.form_submit_button("授業を追加")

                    if submitted and new_subject_name:
                        full_row = [
                            "", new_subject_name, "", new_teacher_name, "", "", "",
                            "", semester, "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                            "", "", ""
                        ]
                        try:
                            sheet.append_row(full_row)
                            st.success(f"授業「{new_subject_name}」を追加しました ✅")
                        except Exception as e:
                            st.error("授業の追加に失敗しました。")
                            st.exception(e)
        else:
            st.dataframe(df)
    except Exception as e:
        st.error("授業データの取得に失敗しました。")
        st.exception(e)
