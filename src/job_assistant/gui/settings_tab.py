"""Settings tab: API keys, location, files, resume page count."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QFileDialog, QHBoxLayout, QLabel, QMessageBox,
)

from ..config import Settings


class SettingsTab(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        form = QFormLayout()

        self.gemini_key = QLineEdit(settings.gemini_api_key)
        self.gemini_key.setEchoMode(QLineEdit.Password)
        self.adzuna_id = QLineEdit(settings.adzuna_app_id)
        self.adzuna_key = QLineEdit(settings.adzuna_app_key)
        self.adzuna_key.setEchoMode(QLineEdit.Password)
        self.jsearch_key = QLineEdit(settings.jsearch_api_key)
        self.jsearch_key.setEchoMode(QLineEdit.Password)

        self.location_mode = QComboBox()
        self.location_mode.addItems(["open_to_relocate", "remote", "specific"])
        self.location_mode.setCurrentText(settings.location_mode)
        self.location = QLineEdit(settings.location)
        self.location_label = QLabel("Specific location:")
        self.location_mode.currentTextChanged.connect(self._toggle_location)
        self._toggle_location(settings.location_mode)

        self.resume_path = QLineEdit(settings.resume_path)
        self.knowledge_path = QLineEdit(settings.knowledge_path)
        self.resume_pages = QSpinBox()
        self.resume_pages.setRange(1, 10)
        self.resume_pages.setValue(settings.resume_pages)
        self.keywords = QLineEdit(settings.keywords)

        form.addRow("Gemini API key:", self.gemini_key)
        form.addRow("Adzuna app id:", self.adzuna_id)
        form.addRow("Adzuna app key:", self.adzuna_key)
        form.addRow("JSearch API key:", self.jsearch_key)
        form.addRow("Location mode:", self.location_mode)
        form.addRow(self.location_label, self.location)
        form.addRow("Resume file:", self._file_picker(self.resume_path, "Resume files (*.doc *.docx *.pdf)"))
        form.addRow("Knowledge file:", self._file_picker(self.knowledge_path, "Markdown/text (*.md *.txt)"))
        form.addRow("Resume length (pages):", self.resume_pages)
        form.addRow("Default keywords:", self.keywords)

        save_btn = QPushButton("Save settings")
        save_btn.clicked.connect(self.save)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(save_btn)
        layout.addStretch()

    def _file_picker(self, line: QLineEdit, filter_: str) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        btn = QPushButton("Browse…")
        btn.clicked.connect(lambda: self._browse(line, filter_))
        h.addWidget(line)
        h.addWidget(btn)
        return w

    def _browse(self, line: QLineEdit, filter_: str) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", filter_)
        if path:
            line.setText(path)

    def _toggle_location(self, mode: str) -> None:
        visible = mode == "specific"
        self.location.setVisible(visible)
        self.location_label.setVisible(visible)

    def save(self) -> None:
        self.settings.gemini_api_key = self.gemini_key.text().strip()
        self.settings.adzuna_app_id = self.adzuna_id.text().strip()
        self.settings.adzuna_app_key = self.adzuna_key.text().strip()
        self.settings.jsearch_api_key = self.jsearch_key.text().strip()
        self.settings.location_mode = self.location_mode.currentText()
        self.settings.location = self.location.text().strip()
        self.settings.resume_path = self.resume_path.text().strip()
        self.settings.knowledge_path = self.knowledge_path.text().strip()
        self.settings.resume_pages = self.resume_pages.value()
        self.settings.keywords = self.keywords.text().strip()
        self.settings.save()
        QMessageBox.information(self, "Saved", "Settings saved.")
