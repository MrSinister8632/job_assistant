"""Search tab: keywords, count, run search, show status."""

import threading

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QLabel,
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

        self.run_btn = QPushButton("Search jobs")
        self.run_btn.clicked.connect(self.run_search)
        self.status = QLabel("Idle.")

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status)
        layout.addStretch()

    def run_search(self) -> None:
        kw = self.keywords.text().strip()
        if not kw:
            self.status.setText("Enter keywords first.")
            return
        self.run_btn.setEnabled(False)
        self.status.setText("Searching…")

        def work():
            try:
                found, new = jobs_mod.search(self.settings, kw, self.count.value())
                self.signals.done.emit(found, new)
            except Exception as e:  # noqa: BLE001
                self.signals.error.emit(str(e))

        threading.Thread(target=work, daemon=True).start()

    def _on_done(self, found: int, new: int) -> None:
        self.run_btn.setEnabled(True)
        self.status.setText(f"Found {found} jobs, {new} new saved.")

    def _on_error(self, msg: str) -> None:
        self.run_btn.setEnabled(True)
        self.status.setText(f"Error: {msg}")
