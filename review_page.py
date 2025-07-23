import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID
from datetime import datetime


def review_page():
    st.title("🗣️ 授業レビュー（口コミ）ページ")

    student_id = st.session_state.get("current_student_id", None)
    if not student_id:
        st.error("❌ 学籍番号が確認されていません。先に学生情報登録画面で確認してください。")
        if st.button("🏠 ホームに戻る"):
            st.session_state.page = "学生情報登録"
            st.rerun()
        return

    review_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("reviews")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    df_reviews = pd.DataFrame(review_sheet.get_all_records())
    df_lectures = pd.DataFrame(lecture_sheet.get_all_records())

    st.subheader("⭐ レビュー投稿")
    lecture_options = df_lectures["subject_name"].dropna().unique().tolist()
    selected_lecture = st.selectbox("授業を選択", lecture_options)
    review_text = st.text_area("レビュー内容")
    rating = st.slider("評価（1〜5）", 1, 5, 3)

    if st.button("レビューを投稿"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [student_id, selected_lecture, review_text, rating, now]
        review_sheet.append_row(new_row)
        st.success("レビューを投稿しました ✅")
        st.rerun()

    st.subheader("📋 掲載中のレビュー")
    if df_reviews.empty:
        st.info("レビューはまだ投稿されていません。")
    else:
        df_reviews = df_reviews[df_reviews["lecture_name"].isin(lecture_options)]
        for i, row in df_reviews.iterrows():
            st.markdown(f"### {row['lecture_name']}")
            st.write(f"🗣️ {row['review_text']}")
            st.write(f"⭐ 評価: {row['rating']} / 5")
            st.caption(f"投稿日: {row['timestamp']}")

            if row['student_id'] == student_id:
                if st.button("🗑️ 削除", key=f"delete_{i}"):
                    review_sheet.delete_rows(i + 2)  # ヘッダー行が1行目なので+2
                    st.success("レビューを削除しました ✅")
                    st.rerun()
