"""Entry point: launch the Qt application."""

from __future__ import annotations

import sys


def main() -> None:
    from PySide6.QtWidgets import QApplication

    from .gui.app import MainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    from .gui.style import QSS

    app.setStyleSheet(QSS)
    window = MainWindow()
    window.show()

    from .interviews import reminder_text
    from PySide6.QtWidgets import QMessageBox

    reminder = reminder_text()
    if reminder:
        QMessageBox.information(window, "Upcoming interviews", reminder)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
