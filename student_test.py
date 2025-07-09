import streamlit as st
import pandas as pd
import os

CSV_PATH = "student.csv"

def load_students():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        return pd.DataFrame(columns=[
            "student_id", "name", "interests", "total_required_credits", "earned_credits"
        ])

def save_students(df):
    df.to_csv(CSV_PATH, index=False)

def main():
    st.title("🎓 学生情報入力アプリ")

    df = load_students()

    st.header("📝 学生情報を追加")

    with st.form("student_form"):
        student_id = st.text_input("学籍番号")
        name = st.text_input("名前")
        interests_input = st.text_input("興味分野（カンマ区切り）", placeholder="例：物理学,AI,留学")
        total_required_credits = st.number_input("必要単位数", min_value=0, value=124)
        earned_credits = st.number_input("取得済み単位数", min_value=0, value=0)

        submitted = st.form_submit_button("追加する")

        if submitted:
            if student_id and name:
                interests = ";".join([s.strip() for s in interests_input.split(",")])
                new_student = {
                    "student_id": student_id,
                    "name": name,
                    "interests": interests,
                    "total_required_credits": total_required_credits,
                    "earned_credits": earned_credits
                }
                df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
                save_students(df)
                st.success(f"{name} さんの情報を追加しました。")
            else:
                st.error("学籍番号と名前は必須です。")

    st.header("📋 現在の学生一覧")
    st.dataframe(df)

if __name__ == "__main__":
    main()
