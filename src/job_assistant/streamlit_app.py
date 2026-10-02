"""Streamlit entry point: sidebar navigation across pages."""

import sys
from pathlib import Path

import streamlit as st

# streamlit runs this file as a script; make the package importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from job_assistant.pages import settings, search, review, applications

st.set_page_config(page_title="Job Assistant", page_icon="💼", layout="wide")

st.sidebar.title("Job Assistant")

page = st.navigation(
    {
        "Search": [
            st.Page(search.render, title="Search", icon="🔍", default=True),
        ],
        "Review": [
            st.Page(review.render, title="Review jobs", icon="📋"),
        ],
        "Track": [
            st.Page(applications.render, title="Applications & Interviews", icon="📅"),
        ],
        "Configure": [
            st.Page(settings.render, title="Settings", icon="⚙️"),
        ],
    }
)
page.run()
