"""Modern Qt stylesheet applied to the whole app."""

QSS = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #1e1e2e;
}

QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background: #313244;
    color: #cdd6f4;
    padding: 8px 18px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background: #45475a;
    color: #ffffff;
}

QTabBar::tab:hover {
    background: #585b70;
}

QLineEdit, QSpinBox, QComboBox, QTextEdit, QListWidget, QTableWidget {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #585b70;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #89b4fa;
}

QPushButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #b4befe;
}

QPushButton:pressed {
    background-color: #74c7ec;
}

QPushButton:disabled {
    background-color: #45475a;
    color: #7f849c;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #585b70;
    border-radius: 4px;
    background: #313244;
}

QCheckBox::indicator:checked {
    background: #89b4fa;
    border: 1px solid #89b4fa;
}

QTableWidget {
    gridline-color: #45475a;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #45475a;
}

QLabel {
    background: transparent;
}

QDialog {
    background-color: #1e1e2e;
}

QScrollBar:vertical {
    background: #1e1e2e;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
}
"""
