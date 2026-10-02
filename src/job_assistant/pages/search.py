"""Search page."""

import streamlit as st

from job_assistant.config import Settings
from job_assistant import jobs as jobs_mod


def render() -> None:
    st.header("🔍 Search jobs")
    settings = Settings.load()

    keywords = st.text_input("Keywords", settings.keywords or "")
    count = st.number_input("Max results per query", min_value=1, max_value=100, value=20)
    use_resume = st.checkbox("Also derive keywords from my resume", value=False)

    if st.button("Search", type="primary"):
        queries = [keywords.strip()] if keywords.strip() else []
        if use_resume:
            with st.spinner("Deriving queries from your resume…"):
                try:
                    from job_assistant.agents.resume_modifier import read_base_resume
                    from job_assistant.llm import complete

                    resume_text = read_base_resume(settings)
                    derived = complete(
                        settings,
                        f"Resume:\n{resume_text[:4000]}\n\nExtract 3-5 concise job search queries, one per line. Output only the queries.",
                        "You are a job search assistant. Output only queries, one per line.",
                    )
                    queries += [line.strip().strip('-*•"') for line in derived.splitlines() if line.strip()]
                except Exception as e:  # noqa: BLE001
                    st.error(f"Could not derive resume keywords: {e}")
                    return
        if not queries:
            st.warning("Enter keywords or enable the resume option.")
            return

        total_found, total_new = 0, 0
        with st.spinner(f"Searching {len(queries)} quer{'y' if len(queries)==1 else 'ies'}…"):
            for q in queries:
                found, new = jobs_mod.search(settings, q, int(count))
                total_found += found
                total_new += new
        st.success(f"Found {total_found} jobs, {total_new} new saved.")
        st.session_state["last_search"] = queries

    if "last_search" in st.session_state:
        st.caption("Last queries: " + " | ".join(st.session_state["last_search"]))
