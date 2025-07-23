import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def profile_edit_page():
    st.title("📝 プロフィール編集 + 履修管理")

    # セッションから student_id 取得
    student_id = st.session_state.get("current_student_id", None)

    if not student_id:
        st.error("❌ 学籍番号が確認されていません。先に学生情報登録画面で確認してください。")
        if st.button("🏠 ホームに戻る"):
            st.session_state.page = "学生情報登録"
            st.rerun()
        return

    # スプレッドシート接続
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")

    students = student_sheet.get_all_records()
    lectures = lecture_sheet.get_all_records()

    df_students = pd.DataFrame(students)
    df_lectures = pd.DataFrame(lectures)

    student_row = df_students[df_students["student_id"] == student_id]

    if not student_row.empty:
        student_data = student_row.iloc[0]
        st.success(f"ようこそ、{student_data['name']} さん！")

        # 現在の履修授業
        raw_subjects = student_data.get("subject_name", "")
        selected_subjects = [s.strip() for s in raw_subjects.split(";") if s.strip()]

        st.subheader("現在の履修授業一覧")
        st.write(selected_subjects if selected_subjects else "（なし）")

        # 履修授業の削除機能
        st.subheader("履修登録を削除")
        if selected_subjects:
            subject_to_remove = st.selectbox("削除したい授業を選択", selected_subjects, key="remove_select")
            if st.button("この授業を削除"):
                selected_subjects.remove(subject_to_remove)
                new_subjects = ";".join(selected_subjects)

                idx = df_students.index[df_students["student_id"] == student_id][0]
                df_students.at[idx, "subject_name"] = new_subjects

                # 保存
                student_sheet.clear()
                student_sheet.append_row(df_students.columns.tolist())
                for _, row in df_students.iterrows():
                    student_sheet.append_row(list(row.values))

                st.success(f"授業「{subject_to_remove}」を削除しました ✅")
                st.rerun()

        # 授業検索・追加登録
        st.subheader("授業を追加で履修登録")
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
                selected_subject = st.selectbox(
                    "この中から追加登録する授業を選択",
                    results["subject_name"].unique().tolist()
                )

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

        # 時間割確認
        if selected_subjects:
            st.subheader("🕘 時間割確認")
            selected_lectures = df_lectures[df_lectures["subject_name"].isin(selected_subjects)]
            st.dataframe(selected_lectures[["subject_name", "day_period"]])

            timetable = {}
            conflicts = []
            missing_info_subjects = []

            for _, row in selected_lectures.iterrows():
                day_period = str(row["day_period"]).strip()

                if not day_period:
                    missing_info_subjects.append(row["subject_name"])
                    continue

                if day_period in timetable:
                    conflicts.append((day_period, timetable[day_period], row["subject_name"]))
                else:
                    timetable[day_period] = row["subject_name"]

            # 曜日・時限未登録の授業に対する対応
            if missing_info_subjects:
                st.info("⚠️ 以下の授業は曜日・時限が未登録です。登録してください:")

                for i, subj_name in enumerate(missing_info_subjects):
                    st.write(f"🔹 {subj_name}")

                    input_day = st.text_input(f"{subj_name} の曜日", key=f"input_day_{i}")
                    input_period = st.text_input(f"{subj_name} の時限", key=f"input_period_{i}")

                    if st.button(f"{subj_name} を更新", key=f"update_{i}"):
                        lecture_idx = df_lectures.index[df_lectures["subject_name"] == subj_name].tolist()
                        if lecture_idx:
                            idx = lecture_idx[0]
                            df_lectures.at[idx, "day_period"] = f"{input_day}-{input_period}"

                            # 保存
                            lecture_sheet.clear()
                            lecture_sheet.append_row(df_lectures.columns.tolist())
                            for _, row in df_lectures.iterrows():
                                lecture_sheet.append_row(list(row.values))

                            st.success(f"{subj_name} の曜日・時限を更新しました ✅")
                            st.rerun()
                        else:
                            st.error(f"授業「{subj_name}」が lecture シートに見つかりません。")

            # 時間割の重複チェック
            if conflicts:
                st.warning("⚠️ 以下の時間に授業が重複しています:")
                for day_period, subj1, subj2 in conflicts:
                    st.write(f"- {day_period}: 「{subj1}」 と 「{subj2}」")
            else:
                st.info("✅ 時間割に重複はありません。")

    else:
        st.error(f"❌ 学籍番号 {student_id} は student シートに存在しません。")

    if st.button("🏠 ホームに戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()