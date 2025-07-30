import streamlit as st
import pandas as pd
from datetime import datetime

def review_page(client, SPREADSHEET_ID):
    st.title("🗣️ 授業レビュー（口コミ）ページ")

    # ✅ 学籍番号の確認（セッションから取得）
    student_id = st.session_state.get("student_id", None)
    if not student_id:
        st.error("❌ 学籍番号が確認されていません。先に学生情報登録画面で確認してください。")
        if st.button("🏠 ホームに戻る"):
            st.session_state.page = "学生情報登録"
            st.rerun()
        return

    # 📄 スプレッドシートの読み込み
    review_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("reviews")
    lecture_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")

    df_reviews = pd.DataFrame(review_sheet.get_all_records())
    df_lectures = pd.DataFrame(lecture_sheet.get_all_records())
    df_students = pd.DataFrame(student_sheet.get_all_records())

    # 学生の名前取得
    student_name = df_students[df_students["student_id"] == student_id]["name"].values[0]

    # ⭐ 投稿セクション
    st.subheader("⭐ レビュー投稿")

    lecture_options = df_lectures["subject_name"].dropna().unique().tolist()
    selected_lecture = st.selectbox("授業を選択", lecture_options)
    review_text = st.text_area("レビュー内容")
    rating = st.slider("評価（1〜5）", 1, 5, 3)

    if st.button("レビューを投稿"):
        selected_row = df_lectures[df_lectures["subject_name"] == selected_lecture].iloc[0]
        class_id = selected_row["class_id"]
        teacher_name = selected_row.get("teacher_name1", "")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [class_id, selected_lecture, teacher_name, review_text, student_id, student_name, rating, now]
        review_sheet.append_row(new_row)
        st.success("レビューを投稿しました ✅")
        st.rerun()

    # 📋 掲載レビュー一覧
    st.subheader("📋 掲載中のレビュー")

    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("キーワードで検索（授業名、教員名、レビュー）")
    with col2:
        min_rating = st.selectbox("評価がこの点以上", [1, 2, 3, 4, 5], index=2)

    if df_reviews.empty:
        st.info("レビューはまだ投稿されていません。")
    else:
        df_reviews = df_reviews[df_reviews["subject_name"].isin(lecture_options)]
        df_reviews = df_reviews[df_reviews["rating"] >= min_rating]

        if search_query:
            df_reviews = df_reviews[
                df_reviews["subject_name"].str.contains(search_query, case=False, na=False) |
                df_reviews["teacher_name"].str.contains(search_query, case=False, na=False) |
                df_reviews["review"].str.contains(search_query, case=False, na=False)
            ]

        if df_reviews.empty:
            st.warning("条件に一致するレビューは見つかりませんでした。")
        else:
            for i, row in df_reviews.iterrows():
                st.markdown(f"### {row['subject_name']}")
                st.write(f"👨‍🏫 教員: {row['teacher_name']}")
                st.write(f"🗣️ {row['review']}")
                st.write(f"⭐ 評価: {row['rating']} / 5")
                st.caption(f"投稿者: {row['name']}　投稿日: {row['timestamp']}")

                if row["student_id"] == student_id:
                    if st.button("🗑️ 自分のレビューを削除", key=f"delete_{i}"):
                        review_sheet.delete_rows(i + 2)  # ヘッダー行を除いた +2
                        st.success("レビューを削除しました ✅")
                        st.rerun()
