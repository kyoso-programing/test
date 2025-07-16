import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報
CREDENTIALS_FILE = "student-465406-8c6c35e39ecf.json"
SPREADSHEET_ID = "1ia3ljvxeVCgZo5gXryN96yHHlDwlv6THmLDmM8UiI1U"
WORKSHEET_NAME = "student"

# Google Sheets接続
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)
    return sheet

# Streamlit アプリ本体
def main():
    st.title("🎓 学生情報登録（Google Sheets append_row 版）")

    sheet = connect_to_sheet()

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
                new_row = [
                    student_id,
                    name,
                    interests,
                    total_required_credits,
                    earned_credits
                ]
                try:
                    sheet.append_row(new_row)
                    st.success(f"{name} さんの情報を追加しました ✅")
                except Exception as e:
                    st.error("スプレッドシートへの保存に失敗しました。")
                    st.exception(e)
            else:
                st.warning("学籍番号と名前は必須です。")

if __name__ == "__main__":
    main()
