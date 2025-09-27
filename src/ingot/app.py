# src/ingot/app.py

from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QMenuBar
from PyQt6.QtGui import QIcon, QAction # Import QAction for type hinting

from .workspace import WorkspaceManager
from .theming.manager import ThemeManager
from .views.base import BaseView
# --- MODIFICATION START ---
# Replace the MenuBarManager with the new ActionManager
from .actions.manager import ActionManager
# --- MODIFICATION END ---
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

        # --- MODIFICATION START ---
        # Initialize the ActionManager and Display
        self.action_manager = ActionManager(self)
        self.display = Display()

        # Create the menu bar. It starts empty.
        self.setMenuBar(QMenuBar(self))

        # Pass the ActionManager to the ThemeManager
        self.theme_manager = ThemeManager(self, self.action_manager)
        # --- MODIFICATION END ---

        self.workspace = WorkspaceManager(view_factory=view_factory)

        # Set up the main layout
        self.display.set_main_widget(self.workspace)
        self.setCentralWidget(self.display)

        # --- MODIFICATION START ---
        # Apply user theme, which now also builds the 'View' menu
        self.theme_manager.apply_theme("theme")
        # --- MODIFICATION END ---

    def set_menu(self, menu_data: dict):
        """Builds and sets the main menu bar from a dictionary."""
        # --- MODIFICATION START ---
        # Use the ActionManager to build the menu
        self.action_manager.build_menu_from_dict(menu_data, self.menuBar())
        # --- MODIFICATION END ---

    # --- NEW METHOD ---
    def get_action(self, action_id: str) -> QAction | None:
        """Public accessor for retrieving a registered action."""
        return self.action_manager.get_action(action_id)
    # --- END NEW METHOD ---

    def set_side_panel(self, widget, position: str = 'left'):
        """Adds a widget to the side panel."""
        self.display.set_side_panel(widget, position)

    def _load_configuration(self, config: dict | None):
        # This method's content remains unchanged.
        self.setWindowTitle("Ingot Application")
        if config:
            self.setWindowTitle(config.get("title", "Ingot Application"))
            if "icon" in config:
                try:
                    from rune import assets
                    import logging
                    icon_path_str = config["icon"]
                    path_parts = icon_path_str.split('.')
                    current_asset = assets
                    for part in path_parts:
                        current_asset = getattr(current_asset, part)
                    icon_path = current_asset
                    self.setWindowIcon(QIcon(str(icon_path)))
                except ImportError:
                    logging.warning("rune-lib is not installed. Cannot load the application icon.")
                except (AttributeError, FileNotFoundError):
                    logging.warning(f"Icon asset path '{config['icon']}' could not be found.")
