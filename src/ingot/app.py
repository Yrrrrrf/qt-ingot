from pathlib import Path
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from .workspace import WorkspaceManager
from .theming.manager import ThemeManager
from .views.base import BaseView  # For type hinting
from .menu.manager import MenuBarManager
from .display import Display


class IngotApp(QMainWindow):
    """
    The main application window, providing the core structure.
    It integrates a workspace, theming, and basic window management.
    """

    def __init__(self, view_factory: type[BaseView], config: dict | None = None):
        super().__init__()
        self.resize(1080, 720)
        self._load_configuration(config)

        # Initialize managers and display
        self.menu_manager = MenuBarManager()
        self.display = Display()

        # Create the menu bar before the theme manager so it can be passed
        self.menu_bar = self.menu_manager.build_from_dict({})
        self.setMenuBar(self.menu_bar)

        self.theme_manager = ThemeManager(self, self.menu_bar)
        self.workspace = WorkspaceManager(view_factory=view_factory)

        # Set up the main layout
        self.display.set_main_widget(self.workspace)
        self.setCentralWidget(self.display)

        # Apply the user's theme by default
        self.theme_manager.apply_theme("theme")

    def set_menu(self, menu_data: dict):
        """Builds and sets the main menu bar from a dictionary."""
        self.menu_manager.build_from_dict(menu_data, self.menu_bar)

    def set_side_panel(self, widget, position: str = 'left'):
        """Adds a widget to the side panel."""
        self.display.set_side_panel(widget, position)

    def _load_configuration(self, config: dict | None):
        """Loads configuration from a dictionary or a JSON file."""
        # Default values
        self.setWindowTitle("Ingot Application")

        if config:
            self.setWindowTitle(config.get("title", "Ingot Application"))
            if "icon" in config:
                # Assuming rune-lib is available to resolve the icon path
                try:
                    from rune import rune
                    icon_path = rune.img(config["icon"])
                    self.setWindowIcon(QIcon(str(icon_path)))
                except ImportError:
                    print("Warning: rune-lib not found. Cannot load icon from path.")
                except FileNotFoundError:
                    print(f"Warning: Icon '{config['icon']}' not found.")