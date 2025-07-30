import streamlit as st
import pandas as pd

def student_page(client, SPREADSHEET_ID):
    st.title("🏠 学生情報登録 / 確認")

    # セッション初期化
    if "current_student_id" not in st.session_state:
        st.session_state.current_student_id = None

    student_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("student")
    students = student_sheet.get_all_records()
    df_students = pd.DataFrame(students)

    if st.session_state.current_student_id:
        # セッションに student_id が保存されていればすぐ次に進める
        student_id = st.session_state.current_student_id
        student_row = df_students[df_students["student_id"] == student_id]
        student_name = student_row.iloc[0]["name"]
        st.success(f"ようこそ、{student_name} さん！")

        col1, col2, col3, col4 = st.columns(4)
        if col1.button("プロフィール編集"):
            st.session_state.page = "プロフィール編集"
            st.rerun()
        if col2.button("先生検索"):
            st.session_state.page = "先生検索"
            st.rerun()
        if col3.button("授業検索"):
            st.session_state.page = "授業検索"
            st.rerun()
        if col4.button("口コミ"):
            st.session_state.page = "口コミ"
            st.rerun()
    else:
        # まだログインしていなければ student_id 入力を要求
        student_id = st.text_input("あなたの学籍番号を入力")

        if student_id:
            student_row = df_students[df_students["student_id"] == student_id]

            if not student_row.empty:
                student_name = student_row.iloc[0]["name"]
                st.session_state.current_student_id = student_id  # セッションに保存
                st.success(f"ようこそ、{student_name} さん！次に進めます。")
                st.rerun()

            else:
                st.warning(f"学籍番号 {student_id} は未登録です。名前を入力して登録してください。")
                name = st.text_input("名前", key="name_input")

                if st.button("新規登録"):
                    if name:
                        new_row = [student_id, name, "", 124, 0]
                        student_sheet.append_row(new_row)
                        st.session_state.current_student_id = student_id  # セッションに保存
                        st.success(f"{name} さんを新規登録しました ✅")
                        st.rerun()
                    else:
                        st.warning("名前を入力してください。")
