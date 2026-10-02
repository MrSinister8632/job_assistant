"""Review tab (placeholder until scoring is implemented)."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReviewTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Job review will be implemented in step 3."))
        layout.addStretch()
