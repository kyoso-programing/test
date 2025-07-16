import streamlit as st
import pandas as pd
from auth import client, SPREADSHEET_ID

def teacher_page():
    st.title("👨‍🏫 先生検索")
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("teacher")
        teachers = sheet.get_all_records()
        df = pd.DataFrame(teachers)

        search_name = st.text_input("先生の名前で検索")
        if search_name:
            results = df[df['teacher_name'].str.contains(search_name, case=False, na=False)]
            st.dataframe(results)

            if results.empty:
                st.info("該当する先生が見つかりません。新しく追加できます。")

                with st.form("add_teacher_form"):
                    new_teacher_name = st.text_input("新しい先生の名前", value=search_name)
                    mail_adress = st.text_input("メールアドレス")
                    academic_field = st.text_input("専門分野")
                    faculty = st.text_input("所属学部")
                    laboratory = st.text_input("研究室名")
                    fulltime_or_not = st.selectbox("専任/非常勤", ["専任", "非常勤"])

                    submitted = st.form_submit_button("先生を追加")

                    if submitted and new_teacher_name:
                        full_row = [
                            new_teacher_name, mail_adress, academic_field, "",
                            faculty, "", "", laboratory, fulltime_or_not
                        ]
                        try:
                            sheet.append_row(full_row)
                            st.success(f"先生「{new_teacher_name}」を追加しました ✅")
                        except Exception as e:
                            st.error("先生の追加に失敗しました。")
                            st.exception(e)
        else:
            st.dataframe(df)
    except Exception as e:
        st.error("先生データの取得に失敗しました。")
        st.exception(e)
