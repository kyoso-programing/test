import streamlit as st
import pandas as pd
import unicodedata
import plotly.graph_objects as go

def normalize_day_period(dp):
    dp = unicodedata.normalize('NFKC', str(dp)).replace(" ", "").replace("　", "")
    return dp

def profile_edit_page(df_lectures, df_students, student_sheet, student_id):
    st.sidebar.markdown("### 🔁 他のページへ移動")
    if st.sidebar.button("🏠 学生情報登録"):
        st.session_state.page = "学生情報登録"
        st.rerun()
    if st.sidebar.button("👨‍🏫 先生検索"):
        st.session_state.page = "先生検索"
        st.rerun()
    if st.sidebar.button("📖 授業検索"):
        st.session_state.page = "授業検索"
        st.rerun()
    if st.sidebar.button("🗣️ 口コミ"):
        st.session_state.page = "口コミ"
        st.rerun()

    st.header("🗓️ 時間割と履修管理")

    # 学生の履修中 class_ids を取得
    student_row = df_students[df_students['student_id'] == student_id]
    current_ids = []
    if not student_row.empty:
        current_ids = str(student_row.iloc[0].get('class_ids', '')).split(';') if student_row.iloc[0].get('class_ids') else []

    # display_label を生成（subject_name + teacher + semester + day_period）
    df_lectures["display_label"] = df_lectures.apply(
        lambda row: f"{row['subject_name']}（{row['teacher_name1']}）[{row['semester']}・{normalize_day_period(row['day_period'])}]", axis=1
    )
    display_to_id = dict(zip(df_lectures["display_label"], df_lectures["class_id"].astype(str)))
    id_to_display = {v: k for k, v in display_to_id.items()}

    # 履修中データ抽出
    selected_lectures = df_lectures[df_lectures["class_id"].astype(str).isin(current_ids)]

    # --- 時間割表示 ---
    st.subheader("📅 現在の時間割")
    selected_semester = st.selectbox("表示する学期を選択", ["春", "夏", "秋", "冬"])
    sem_df = selected_lectures[selected_lectures["semester"] == selected_semester]
    timetable = {f"{i}限": {d: [] for d in "月火水木金"} for i in range(1, 6)}

    for _, row in sem_df.iterrows():
        label = f"{row['subject_name']}\n{row['teacher_name1']}"
        class_id = str(row['class_id'])
        for slot in str(row['day_period']).split(','):
            slot = normalize_day_period(slot.strip())
            if len(slot) >= 2 and slot[0] in "月火水木金" and slot[1:].isdigit():
                day = slot[0]
                period = f"{slot[1:]}限"
                timetable[period][day].append((class_id, label))

    fig = go.Figure()
    days = list("月火水木金")
    periods = list(timetable.keys())
    cell_text = []
    for period in periods:
        row = []
        for day in days:
            cell = timetable[period][day]
            if not cell:
                row.append("")
            else:
                texts = []
                for cid, label in cell:
                    btn = st.button(f"🗑 {label}", key=f"del_{selected_semester}_{day}_{period}_{cid}")
                    if btn:
                        current_ids = [id for id in current_ids if id != cid]
                        df_students.loc[df_students['student_id'] == student_id, 'class_ids'] = ';'.join(current_ids)
                        student_sheet.update_cell(student_row.index[0] + 2, df_students.columns.get_loc("class_ids") + 1, ';'.join(current_ids))
                        st.rerun()
                    texts.append(label)
                row.append("\n".join(texts))
        cell_text.append(row)

    fig.add_trace(go.Table(
        header=dict(values=[""] + days, fill_color="black", font=dict(color="white"), align="center"),
        cells=dict(values=[[p for p in periods]] + list(map(list, zip(*cell_text))), fill_color="#111", font=dict(color="white"), align="center")
    ))
    st.plotly_chart(fig, use_container_width=True, key=f"tt_{selected_semester}")

    # --- 登録セクション ---
    st.subheader("📚 履修登録")
    unregistered = df_lectures[~df_lectures["class_id"].astype(str).isin(current_ids)]
    options = unregistered["display_label"].tolist()
    selected_label = st.selectbox("追加したい授業を選んでください", [""] + options)
    if selected_label and selected_label in display_to_id:
        selected_class_id = display_to_id[selected_label]
        current_ids.append(selected_class_id)
        df_students.loc[df_students['student_id'] == student_id, 'class_ids'] = ';'.join(current_ids)
        student_sheet.update_cell(student_row.index[0] + 2, df_students.columns.get_loc("class_ids") + 1, ';'.join(current_ids))
        st.success("授業を追加しました")
        st.rerun()

    # --- 削除セクション ---
    st.subheader("🗑️ 履修削除")
    selected_labels = st.multiselect("削除したい授業を選んでください", [id_to_display[cid] for cid in current_ids if cid in id_to_display])
    if st.button("選択した授業を削除") and selected_labels:
        delete_ids = [display_to_id[label] for label in selected_labels if label in display_to_id]
        current_ids = [cid for cid in current_ids if cid not in delete_ids]
        df_students.loc[df_students['student_id'] == student_id, 'class_ids'] = ';'.join(current_ids)
        student_sheet.update_cell(student_row.index[0] + 2, df_students.columns.get_loc("class_ids") + 1, ';'.join(current_ids))
        st.success("削除しました")
        st.rerun()
