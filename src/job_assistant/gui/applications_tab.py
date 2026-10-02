"""Applications tab (placeholder until tracker is implemented)."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ApplicationsTab(QWidget):
    def __init__(self, settings=None, parent=None):
        super().__init__(parent)
        self.settings = settings
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Application tracking will be implemented in step 7."))
        layout.addStretch()
