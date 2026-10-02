"""Search tab: keywords, count, run search, show status."""

import threading

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QLabel,
    QCheckBox,
)

from ..config import Settings
from .. import jobs as jobs_mod


class _WorkerSignals(QObject):
    done = Signal(int, int)
    error = Signal(str)


class SearchTab(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.signals = _WorkerSignals()
        self.signals.done.connect(self._on_done)
        self.signals.error.connect(self._on_error)

        form = QFormLayout()
        self.keywords = QLineEdit(settings.keywords)
        self.count = QSpinBox()
        self.count.setRange(1, 100)
        self.count.setValue(20)
        form.addRow("Keywords:", self.keywords)
        form.addRow("Max results:", self.count)
        self.use_resume_keywords = QCheckBox("Also derive keywords from my resume")
        form.addRow("", self.use_resume_keywords)

        self.run_btn = QPushButton("Search jobs")
        self.run_btn.clicked.connect(self.run_search)
        self.status = QLabel("Idle.")

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status)
        layout.addStretch()

    def run_search(self) -> None:
        manual = self.keywords.text().strip()
        use_resume = self.use_resume_keywords.isChecked()
        if not manual and not use_resume:
            self.status.setText("Enter keywords first.")
            return
        self.run_btn.setEnabled(False)
        self.status.setText("Searching…")

        def work():
            try:
                queries = [manual] if manual else []
                if use_resume:
                    try:
                        from ..agents.resume_modifier import read_base_resume
                        from ..llm import complete

                        resume_text = read_base_resume(self.settings)
                        derived = complete(
                            self.settings,
                            f"Resume:\n{resume_text[:4000]}\n\nExtract 3-5 concise job search queries "
                            "(e.g. 'python backend developer'), one per line. Output only the queries, one per line.",
                            "You are a job search assistant. Output only queries, one per line.",
                        )
                        queries += [line.strip().strip('-*•"') for line in derived.splitlines() if line.strip()]
                    except Exception as e:  # noqa: BLE001
                        self.signals.error.emit(f"Could not derive resume keywords: {e}")
                        return
                total_found, total_new = 0, 0
                for q in queries:
                    found, new = jobs_mod.search(self.settings, q, self.count.value())
                    total_found += found
                    total_new += new
                self.signals.done.emit(total_found, total_new)
            except Exception as e:  # noqa: BLE001
                self.signals.error.emit(str(e))

        threading.Thread(target=work, daemon=True).start()

    def _on_done(self, found: int, new: int) -> None:
        self.run_btn.setEnabled(True)
        self.status.setText(f"Found {found} jobs, {new} new saved.")

    def _on_error(self, msg: str) -> None:
        self.run_btn.setEnabled(True)
        self.status.setText(f"Error: {msg}")
