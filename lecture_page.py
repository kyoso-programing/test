import streamlit as st
import pandas as pd

def lecture_page(client, SPREADSHEET_ID):
    st.title("📖 授業検索・登録")

    # データ取得
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    df_lectures = pd.DataFrame(lecture_sheet.get_all_records())

    # 🔍 テキスト検索
    keyword = st.text_input("授業名・教員名・キーワードで検索")
    
    # 📅 学期フィルタ
    semesters = df_lectures["semester"].dropna().unique().tolist()
    semester_filter = st.selectbox("学期で絞り込む", ["すべて"] + semesters)

    # 🕒 時間帯フィルタ（複数選択可）
    all_day_periods = sorted(set(dp.strip() for val in df_lectures["day_period"].dropna() for dp in str(val).split(',')))
    day_period_filter = st.multiselect("曜日・時限で絞り込む（例: 月1, 水3）", all_day_periods)

    # フィルタ処理
    if keyword:
        keyword = keyword.lower()
        df_lectures = df_lectures[
            df_lectures["subject_name"].str.lower().str.contains(keyword, na=False) |
            df_lectures["teacher_name1"].str.lower().str.contains(keyword, na=False) |
            df_lectures.get("keyword", "").astype(str).str.lower().str.contains(keyword, na=False)
        ]
    if semester_filter != "すべて":
        df_lectures = df_lectures[df_lectures["semester"] == semester_filter]

    if day_period_filter:
        df_lectures = df_lectures[
            df_lectures["day_period"].apply(lambda x: any(dp.strip() in str(x) for dp in day_period_filter))
        ]

    # 学生ID処理
    student_id = st.session_state.get("student_id")
    df_students = pd.DataFrame()
    student_row = pd.DataFrame()
    current_ids = []

    if student_id:
        student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
        df_students = pd.DataFrame(student_sheet.get_all_records())
        student_row = df_students[df_students["student_id"] == student_id]
        if not student_row.empty:
            current_ids = str(student_row.iloc[0].get("class_ids", "")).split(';') if student_row.iloc[0].get("class_ids") else []
    else:
        st.info("🔓 ログインしていないため、授業の閲覧は可能ですが、履修登録はできません。")

    # 表示
    for _, row in df_lectures.iterrows():
        class_id = str(row["class_id"])
        is_registered = class_id in current_ids

        faculty = row.get("faculty", "未設定")
        comment = row.get("comments", "なし")

        with st.expander(f"{row['subject_name']}（{row['teacher_name1']}）[{row['semester']}・{row['day_period']}]"):
            st.write(f"📚 教員: {row['teacher_name1']}")
            st.write(f"🕒 学期: {row['semester']} / 時間帯: {row['day_period']}")
            st.write(f"🏛 所属: {faculty}")
            st.write(f"💬 備考: {comment}")

            if not student_id:
                st.warning("ログインしていないため履修登録できません。")
            elif is_registered:
                st.info("✅ この授業はすでに履修済みです。")
            else:
                if st.button("📌 履修登録する", key=f"add_{class_id}"):
                    current_ids.append(class_id)
                    new_ids = ';'.join(current_ids)
                    df_students.loc[df_students["student_id"] == student_id, "class_ids"] = new_ids
                    student_sheet.update_cell(student_row.index[0] + 2, df_students.columns.get_loc("class_ids") + 1, new_ids)
                    st.success("履修登録しました！")
                    st.rerun()
