import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証と接続設定
CREDENTIALS_FILE = "student-465406-8c6c35e39ecf.json"
SPREADSHEET_ID = "1ia3ljvxeVCgZo5gXryN96yHHlDwlv6THmLDmM8UiI1U"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# expected_headers for lecture sheet
LECTURE_HEADERS = [
    "class_id", "subject_name", "class_name",
    "teacher_name1", "teacher_name2", "teacher_name3", "teacher_name4",
    "class_category", "semester", "day", "period", "keyword", "place", "language",
    "class_satisfaction", "class_difficulty", "textbook", "test_report",
    "test_bringingin", "test_times", "test_difficulty", "comments",
    "course_requirements", "attendance", "evaluation_criteria",
    "class_credit", "student_number", "class_style"
]

# ページ切り替え
st.sidebar.title("メニュー")
page = st.sidebar.selectbox("ページを選択", ["学生情報登録", "授業検索", "先生検索"])

if page == "学生情報登録":
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


elif page == "授業検索":
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

elif page == "先生検索":
    st.title("👨‍🏫 先生検索")
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("teacher")
        teachers = sheet.get_all_records()
        df = pd.DataFrame(teachers)

        search_name = st.text_input("先生の名前で検索")
        if search_name:
            results = df[df['teacher_name'].str.contains(search_name, case=False, na=False)]
            st.dataframe(results)

            if results.empty:
                st.info("該当する先生が見つかりません。新しく追加できます。")

                with st.form("add_teacher_form"):
                    new_teacher_name = st.text_input("新しい先生の名前", value=search_name)
                    mail_adress = st.text_input("メールアドレス")
                    academic_field = st.text_input("専門分野")
                    faculty = st.text_input("所属学部")
                    laboratory = st.text_input("研究室名")
                    fulltime_or_not = st.selectbox("専任/非常勤", ["専任", "非常勤"])

                    submitted = st.form_submit_button("先生を追加")

                    if submitted and new_teacher_name:
                        full_row = [
                            new_teacher_name, mail_adress, academic_field, "",
                            faculty, "", "", laboratory, fulltime_or_not
                        ]
                        try:
                            sheet.append_row(full_row)
                            st.success(f"先生「{new_teacher_name}」を追加しました ✅")
                        except Exception as e:
                            st.error("先生の追加に失敗しました。")
                            st.exception(e)
        else:
            st.dataframe(df)
    except Exception as e:
        st.error("先生データの取得に失敗しました。")
        st.exception(e)
