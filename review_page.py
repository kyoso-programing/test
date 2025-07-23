import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def review_page():
    st.title("💬 口コミ投稿・閲覧")

    student_id = st.session_state.get("current_student_id", None)
    if not student_id:
        st.error("❌ 学籍番号が確認されていません。先に学生情報登録画面で確認してください。")
        if st.button("🏠 ホームに戻る"):
            st.session_state.page = "学生情報登録"
            st.rerun()
        return

    # スプレッドシート読み込み
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    review_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("reviews")

    df_students = pd.DataFrame(student_sheet.get_all_records())
    df_lectures = pd.DataFrame(lecture_sheet.get_all_records())
    df_reviews = pd.DataFrame(review_sheet.get_all_records())

    # 現在の学生データ
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
        rating = st.slider("評価 (1〜5)", 1, 5, 3)
        comment = st.text_area("口コミを入力")

        if st.button("口コミを投稿"):
            if comment.strip():
                lecture_row = df_lectures[df_lectures["subject_name"] == selected_subject]
                class_id = str(lecture_row.iloc[0]["class_id"]) if not lecture_row.empty else ""

                new_row = [class_id, selected_subject, comment.strip(), student_id, student_name, rating]
                try:
                    review_sheet.append_row(new_row)
                    st.success(f"「{selected_subject}」への口コミを投稿しました ✅")
                    st.rerun()
                except Exception as e:
                    st.error("口コミの保存に失敗しました。")
                    st.exception(e)
            else:
                st.warning("コメントを入力してください。")
    else:
        st.info("履修授業がまだありません。")

    # 口コミ表示
    st.subheader("他のユーザーの口コミを見る")
    search_query = st.text_input("授業名で口コミを検索")

    if not df_reviews.empty:
        df_reviews["student_id"] = df_reviews["student_id"].astype(str)
        df_reviews["rating"] = pd.to_numeric(df_reviews.get("rating", 0), errors="coerce").fillna(0).astype(int)

        df_display = df_reviews.copy()
        if search_query:
            df_display = df_display[df_display["subject_name"].str.contains(search_query, case=False, na=False)]

        if not df_display.empty:
            for i, row in df_display.iterrows():
                st.markdown(f"### {row['subject_name']}")
                st.markdown(f"🧑‍🎓 {row['name']} | ⭐ 評価: {row['rating']}")
                st.markdown(f"💬 {row['review']}")

                if str(row['student_id']) == str(student_id):
                    if st.button("🗑️ この口コミを削除", key=f"delete_{i}"):
                        df_reviews = df_reviews[
                            ~(
                                (df_reviews["student_id"] == student_id) &
                                (df_reviews["review"] == row['review']) &
                                (df_reviews["subject_name"] == row['subject_name'])
                            )
                        ]
                        review_sheet.clear()
                        review_sheet.append_row(df_reviews.columns.tolist())
                        for _, r in df_reviews.iterrows():
                            review_sheet.append_row(list(r.values))
                        st.success("口コミを削除しました ✅")
                        st.rerun()
        else:
            st.info("該当する口コミが見つかりません。")
    else:
        st.info("まだ口コミはありません。")

    if st.button("🏠 ホームに戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
