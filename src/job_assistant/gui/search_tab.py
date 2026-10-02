"""Search tab (placeholder until job fetching is implemented)."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SearchTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Job search will be implemented in step 2."))
        layout.addStretch()
