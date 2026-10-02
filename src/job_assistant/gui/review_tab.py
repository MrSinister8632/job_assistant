"""Review tab: list jobs from DB with scores and summaries, selectable."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QListWidgetItem, QTextEdit,
)
from PySide6.QtCore import Qt

from ..config import Settings
from ..storage import get_conn


class ReviewTab(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings

        self.list = QListWidget()
        self.list.itemChanged.connect(lambda *_: None)
        self.list.currentItemChanged.connect(self._show)
        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        self.selected_label = QLabel("")

        refresh = QPushButton("Refresh list")
        refresh.clicked.connect(self.reload)

        top = QHBoxLayout()
        top.addWidget(self.list, 1)
        top.addWidget(self.detail, 2)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(refresh)
        layout.addWidget(self.selected_label)
        layout.addStretch()
        self.reload()

    def reload(self) -> None:
        self.list.clear()
        conn = get_conn()
        rows = conn.execute(
            "SELECT id, title, company, salary, eligible, score, summary, location, url FROM jobs ORDER BY fetched_at DESC"
        ).fetchall()
        conn.close()
        for r in rows:
            item = QListWidgetItem(f"{r['title']} — {r['company']} ({r['location'] or 'n/a'})  [score: {r['score'] if r['score'] is not None else '?'}]")
            item.setData(0x0100, dict(r))  # Qt.UserRole
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list.addItem(item)
        self.selected_label.setText(f"{len(rows)} jobs loaded.")

    def _show(self, current, _prev) -> None:
        if not current:
            return
        job = current.data(0x0100)
        if not job:
            return
        text = (
            f"<b>{job['title']}</b> — {job['company']}<br>"
            f"<i>{job['location']}</i> | {job['salary'] or 'Pay not specified'}<br><br>"
            f"{(job['summary'] or 'No summary yet.').replace(chr(10), '<br>')}<br><br>"
            f"<a href='{job['url']}'>{job['url']}</a>"
        )
        self.detail.setHtml(text)
