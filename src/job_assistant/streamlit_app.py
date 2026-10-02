"""Streamlit entry point: sidebar navigation across pages."""

import streamlit as st

from pages import settings, search, review, applications

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
