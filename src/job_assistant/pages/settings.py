"""Settings page."""

import streamlit as st

from job_assistant.config import Settings


def render() -> None:
    st.header("⚙️ Settings")
    settings = Settings.load()

    st.subheader("Job search")
    labels = {"open_to_relocate": "Open to relocate", "remote": "Remote only", "specific": "Choose my own"}
    current_label = labels.get(settings.location_mode, labels["open_to_relocate"])
    chosen_label = st.selectbox("Location mode", list(labels.values()), index=list(labels.values()).index(current_label))
    settings.location_mode = next(k for k, v in labels.items() if v == chosen_label)
    if settings.location_mode == "specific":
        settings.location = st.text_input("Your location (city)", settings.location)

    with st.form("settings_form"):
        st.subheader("API keys")
        settings.gemini_api_key = st.text_input("Gemini API key", settings.gemini_api_key, type="password")
        settings.adzuna_app_id = st.text_input("Adzuna app id", settings.adzuna_app_id)
        settings.adzuna_app_key = st.text_input("Adzuna app key", settings.adzuna_app_key, type="password")
        settings.jsearch_api_key = st.text_input("JSearch API key", settings.jsearch_api_key, type="password")

        settings.keywords = st.text_input("Default keywords", settings.keywords)

        st.subheader("Resume")
        settings.resume_path = st.text_input("Resume file path (.doc/.pdf)", settings.resume_path)
        settings.knowledge_path = st.text_input("Knowledge file path (.md)", settings.knowledge_path)
        settings.resume_pages = st.number_input("Resume length (pages)", min_value=1, max_value=10, value=settings.resume_pages)

        if st.form_submit_button("Save settings"):
            settings.save()
            st.success("Settings saved.")
