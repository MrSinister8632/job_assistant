"""Applications tab: saved applications + interviews."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox,
)

from ..config import Settings
from ..storage import get_conn
from .. import interviews as interviews_mod


class ApplicationsTab(QWidget):
    def __init__(self, settings=None, parent=None):
        super().__init__(parent)
        self.settings = settings

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Job", "Company", "Status", "Applied at", "Notes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.reload)
        export_btn = QPushButton("Export interviews (.ics)")
        export_btn.clicked.connect(self._export)
        self.count_label = QLabel("")

        top_btn = QHBoxLayout()
        top_btn.addWidget(refresh)
        top_btn.addWidget(export_btn)
        top_btn.addWidget(self.count_label)
        top_btn.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(top_btn)
        layout.addWidget(self.table)
        self.reload()

    def reload(self) -> None:
        conn = get_conn()
        rows = conn.execute(
            """SELECT j.title, j.company, a.status, a.applied_at, a.notes
               FROM applications a LEFT JOIN jobs j ON j.id = a.job_id
               ORDER BY a.id DESC"""
        ).fetchall()
        conn.close()
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for col, val in enumerate((r["title"], r["company"], r["status"], r["applied_at"], r["notes"])):
                self.table.setItem(i, col, QTableWidgetItem(str(val or "")))
        self.count_label.setText(f"{len(rows)} applications.")

    def _export(self) -> None:
        path = interviews_mod.export_ics()
        QMessageBox.information(self, "Exported", f"Interviews exported to:\n{path}")
