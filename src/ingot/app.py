from pathlib import Path
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from .workspace import WorkspaceManager
from .theming.manager import ThemeManager
from .views.base import BaseView # For type hinting

class IngotApp(QMainWindow):
    """
    The main application window, providing the core structure.
    It integrates a workspace, theming, and basic window management.
    """
    def __init__(self, view_factory: type[BaseView]):
        super().__init__()
        self.setWindowTitle("Ingot Application")
        self.resize(1080, 720)

        # Initialize core components. Instantiating ThemeManager automatically scaffolds
        # the user's theme directory if it's missing.
        self.theme_manager = ThemeManager(self)
        self.workspace = WorkspaceManager(view_factory=view_factory)
        
        self.setCentralWidget(self.workspace)
        
        # Apply the user's theme by default. The manager will fall back to the
        # bundled theme if the user's theme is not found.
        self.theme_manager.apply_theme(self.theme_manager._user_themes_path / "theme.scss")

    def set_window_icon_from_path(self, icon_path: str | Path):
        """Sets the window icon from a given file path."""
        self.setWindowIcon(QIcon(str(icon_path)))