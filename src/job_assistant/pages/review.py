"""Review jobs page."""

import streamlit as st

from job_assistant.config import Settings
from job_assistant.storage import get_conn


def render() -> None:
    st.header("📋 Review jobs")

    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, company, location, salary, eligible, score, summary, url FROM jobs ORDER BY fetched_at DESC"
    ).fetchall()
    conn.close()

    if not rows:
        st.info("No jobs yet — run a search first.")
        return

    selected = st.session_state.setdefault("selected_jobs", set())
    st.write(f"**{len(rows)} jobs.** Check the ones you want to apply to.")

    for r in rows:
        cols = st.columns([0.05, 0.45, 0.2, 0.15, 0.15])
        checked = cols[0].checkbox("select", value=r["id"] in selected, key=f"sel_{r['id']}", label_visibility="collapsed")
        if checked:
            selected.add(r["id"])
        else:
            selected.discard(r["id"])
        cols[1].markdown(f"**{r['title']}**  ")
        cols[2].write(r["company"])
        cols[3].write(r["location"] or "n/a")
        cols[4].write(f"score: {r['score'] if r['score'] is not None else '—'}")
        with st.expander("Details"):
            st.write(f"**Pay:** {r['salary'] or 'Not specified'}")
            st.write(r["summary"] or "No summary yet.")
            st.markdown(f"[Open posting]({r['url']})")

    st.session_state["selected_jobs"] = selected
    st.divider()
    st.write(f"**{len(selected)} selected.**")
    if st.button("Prepare applications for selected", type="primary"):
        st.session_state["apply_selection"] = list(selected)
        st.success(f"{len(selected)} jobs queued. Use the missing-info form below, then generate.")

    with st.form("missing_info"):
        st.subheader("Details the agent may need")
        extra = {}
        extra["work_authorization"] = st.text_input("Work authorization / sponsorship needs")
        extra["salary_expectation"] = st.text_input("Salary expectation")
        extra["availability"] = st.text_input("Available start date")
        extra["years_experience"] = st.text_input("Years of experience")
        extra["highest_education"] = st.text_input("Highest education")
        extra["willing_to_relocate"] = st.text_input("Willing to relocate? (y/n)")
        if st.form_submit_button("Generate resumes & cover letters"):
            st.session_state["extra_info"] = {k: v for k, v in extra.items() if v}
            st.info("Generation will run from the Applications page (wired in next).")
