import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def review_page():
    st.title("💬 口コミ投稿・閲覧")

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
    review_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("reviews")

    students = student_sheet.get_all_records()
    lectures = lecture_sheet.get_all_records()
    reviews = review_sheet.get_all_records()

    df_students = pd.DataFrame(students)
    df_lectures = pd.DataFrame(lectures)
    df_reviews = pd.DataFrame(reviews)

    # 現在の学生情報
    student_row = df_students[df_students["student_id"] == student_id]
    if student_row.empty:
        st.error(f"学籍番号 {student_id} は student シートに存在しません。")
        return

    student_data = student_row.iloc[0]
    student_name = student_data["name"]
    raw_subjects = student_data.get("subject_name", "")
    enrolled_subjects = [s.strip() for s in raw_subjects.split(";") if s.strip()]

    st.subheader("自分の履修授業から選んで口コミを投稿")

    if enrolled_subjects:
        selected_subject = st.selectbox("口コミを投稿する授業を選択", enrolled_subjects)
        comment = st.text_area("口コミを入力")

        if st.button("口コミを投稿"):
            if comment.strip():
                # class_id を lecture シートから取得
                lecture_row = df_lectures[df_lectures["subject_name"] == selected_subject]
                if not lecture_row.empty:
                    class_id = lecture_row.iloc[0]["class_id"]
                    class_id = str(class_id)
                else:
                    class_id = ""  # 見つからない場合は空白

                new_row = [class_id, selected_subject, comment.strip(), student_id, student_name]
                review_sheet.append_row(new_row)
                st.success(f"「{selected_subject}」への口コミを投稿しました ✅")
            else:
                st.warning("コメントを入力してください。")
    else:
        st.info("履修授業がまだありません。")

    st.subheader("他のユーザーの口コミを見る")

    search_query = st.text_input("授業名で口コミを検索")
    if not df_reviews.empty:
        df_display = df_reviews
        if search_query:
            df_display = df_display[df_display["subject_name"].str.contains(search_query, case=False, na=False)]

        if not df_display.empty:
            st.dataframe(df_display[["subject_name", "name", "review"]])
        else:
            st.info("該当する口コミが見つかりません。")
    else:
        st.info("まだ口コミはありません。")

    if st.button("🏠 ホームに戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
