# timetable_page.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def timetable_page(client, SPREADSHEET_ID):  # ←この関数が必要
    st.title("📅 時間割表示")

    # データ読み込み
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("lecture")
    df = pd.DataFrame(sheet.get_all_records())

    # セメスター（春・夏・秋・冬）
    semesters = ["春", "夏", "秋", "冬"]
    tab_objs = st.tabs([f"{s}学期" for s in semesters])

    for tab, semester in zip(tab_objs, semesters):
        with tab:
            show_timetable(df[df["semester"] == semester], semester)

def show_timetable(df, semester=""):
    days = ["月", "火", "水", "木", "金"]
    periods = ["1限", "2限", "3限", "4限", "5限"]
    timetable = pd.DataFrame("", index=periods, columns=days)

    for _, row in df.iterrows():
        if pd.isna(row["day_period"]): continue
        entry = f"{row['subject_name']}"
        for slot in str(row["day_period"]).split(","):
            if len(slot) >= 2:
                day = slot[0]
                period = slot[1:]
                if day in days and period in periods:
                    timetable.loc[period, day] += entry + "\n"

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[""] + days,
            fill_color="black",
            font=dict(color="white", size=14),
            align="center"
        ),
        cells=dict(
            values=[[p for p in periods]] + [timetable[day].tolist() for day in days],
            fill_color="rgb(30,30,30)",
            font=dict(color="white", size=13),
            align="center",
            height=60
        )
    )])

    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="black")
    st.plotly_chart(fig, use_container_width=True, key=f"timetable_{semester}")
