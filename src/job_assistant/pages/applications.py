"""Applications & interviews page."""

import streamlit as st
import pandas as pd

from job_assistant.config import Settings
from job_assistant.storage import get_conn
from job_assistant import interviews as interviews_mod


def render() -> None:
    st.header("📅 Applications & Interviews")

    reminder = interviews_mod.reminder_text()
    if reminder:
        st.warning(reminder)

    conn = get_conn()
    rows = conn.execute(
        """SELECT j.title, j.company, a.status, a.applied_at, a.notes
           FROM applications a LEFT JOIN jobs j ON j.id = a.job_id
           ORDER BY a.id DESC"""
    ).fetchall()
    conn.close()

    if rows:
        df = pd.DataFrame([dict(r) for r in rows])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No applications tracked yet.")

    if st.button("Export interviews (.ics)"):
        path = interviews_mod.export_ics()
        st.success(f"Exported to {path}")

    st.divider()
    with st.expander("Schedule an interview"):
        app_id = st.number_input("Application ID", min_value=1, step=1)
        when = st.text_input("Date/time (e.g. 2026-10-05T14:30)")
        kind = st.selectbox("Type", ["phone", "video", "onsite"])
        link = st.text_input("Meeting link", "")
        notes = st.text_input("Notes", "")
        if st.button("Save interview"):
            from datetime import datetime

            try:
                interviews_mod.schedule_interview(int(app_id), datetime.fromisoformat(when), kind, link, notes)
                st.success("Interview saved.")
            except ValueError:
                st.error("Bad date/time format — use e.g. 2026-10-05T14:30")
