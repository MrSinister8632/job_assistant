"""Settings page."""

import streamlit as st

from job_assistant.config import Settings


def render() -> None:
    st.header("⚙️ Settings")
    settings = Settings.load()

    with st.form("settings_form"):
        st.subheader("API keys")
        settings.gemini_api_key = st.text_input("Gemini API key", settings.gemini_api_key, type="password")
        settings.adzuna_app_id = st.text_input("Adzuna app id", settings.adzuna_app_id)
        settings.adzuna_app_key = st.text_input("Adzuna app key", settings.adzuna_app_key, type="password")
        settings.jsearch_api_key = st.text_input("JSearch API key", settings.jsearch_api_key, type="password")

        st.subheader("Job search")
        modes = ["open_to_relocate", "remote", "specific"]
        settings.location_mode = st.selectbox(
            "Location mode", modes, index=modes.index(settings.location_mode) if settings.location_mode in modes else 0
        )
        if settings.location_mode == "specific":
            settings.location = st.text_input("Specific location (city)", settings.location)
        settings.keywords = st.text_input("Default keywords", settings.keywords)

        st.subheader("Resume")
        settings.resume_path = st.text_input("Resume file path (.doc/.pdf)", settings.resume_path)
        settings.knowledge_path = st.text_input("Knowledge file path (.md)", settings.knowledge_path)
        settings.resume_pages = st.number_input("Resume length (pages)", min_value=1, max_value=10, value=settings.resume_pages)

        if st.form_submit_button("Save settings"):
            settings.save()
            st.success("Settings saved.")
