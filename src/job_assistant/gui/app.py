"""Main window with the four tabs."""

from PySide6.QtWidgets import QMainWindow, QTabWidget

from ..config import Settings
from .settings_tab import SettingsTab
from .search_tab import SearchTab
from .review_tab import ReviewTab
from .applications_tab import ApplicationsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Assistant")
        self.resize(900, 600)
        self.settings = Settings.load()

        tabs = QTabWidget()
        self.settings_tab = SettingsTab(self.settings)
        tabs.addTab(self.settings_tab, "Settings")
        tabs.addTab(SearchTab(), "Search")
        tabs.addTab(ReviewTab(), "Review")
        tabs.addTab(ApplicationsTab(), "Applications")
        self.setCentralWidget(tabs)
