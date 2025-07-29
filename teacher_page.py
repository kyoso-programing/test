import streamlit as st
import pandas as pd

def teacher_page(client, SPREADSHEET_ID):
    st.title("👨‍🏫 先生検索")

    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("teacher")
        teachers = sheet.get_all_records()
        df = pd.DataFrame(teachers)

        if df.empty:
            st.warning("現在、登録されている先生情報はありません。")
            return

        search_name = st.text_input("先生の名前で検索")

        if search_name:
            results = df[df['teacher_name'].str.contains(search_name, case=False, na=False)]
            if results.empty:
                st.info("該当する先生は見つかりませんでした。")
            else:
                st.dataframe(results)
        else:
            st.dataframe(df)

    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")

    # 🔔 遷移ボタン
    if st.button("🏠 ホーム（学生ページ）に戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
