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

        search_query = st.text_input("🔍 先生の名前・分野・所属で検索")

        if search_query.strip():
            df_filtered = df[
                df["teacher_name"].str.contains(search_query, case=False, na=False) |
                df["academic_field"].str.contains(search_query, case=False, na=False) |
                df["faculty"].str.contains(search_query, case=False, na=False)
            ]
            show_all_fields = True
        else:
            df_filtered = df.copy()
            show_all_fields = False

        if df_filtered.empty:
            st.info("該当する先生は見つかりませんでした。")
        else:
            for _, row in df_filtered.iterrows():
                st.markdown(f"""
                    <div style="background-color:#111; color:#fff; padding:15px; border-radius:10px; margin-bottom:15px;">
                        <h4 style="margin-bottom:5px;">{row['teacher_name']}</h4>
                        <p><strong>専門分野:</strong> {row['academic_field']}</p>
                        <p><strong>所属:</strong> {row['faculty']}</p>
                """, unsafe_allow_html=True)

                if show_all_fields:
                    # 詳細情報をすべて表示
                    for col in df.columns:
                        if col not in ["teacher_name", "academic_field", "faculty"]:
                            value = row[col] if row[col] else "（未記入）"
                            st.markdown(f"<p style='color:white; margin:0;'><strong>{col}:</strong> {value}</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")

    if st.button("🏠 ホーム（学生ページ）に戻る"):
        st.session_state.page = "学生情報登録"
        st.rerun()
