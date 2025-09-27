import sass
from pathlib import Path
import importlib.resources as pkg_resources
from PyQt6.QtWidgets import QWidget, QMenuBar, QMenu
from PyQt6.QtGui import QAction
import shutil
import logging
from rune import assets, AssetNotFoundError

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ThemeManager:
    """Manages the loading, application, and scaffolding of SASS stylesheets."""
    def __init__(self, target_widget: QWidget, menu_bar: QMenuBar):
        self._target = target_widget
        self._menu_bar = menu_bar
        self._discover_and_add_themes_to_menu()



    def _discover_and_add_themes_to_menu(self):
        """Discovers .scss themes using rune-lib and adds them to the 'View' menu."""
        # ... (code to find or create the View -> Themes menu remains the same) ...
        view_menu = self._menu_bar.findChild(QMenu, "View")
        if not view_menu:
            view_menu = QMenu("View", self._menu_bar)
            self._menu_bar.addMenu(view_menu)

        theme_menu = QMenu("Themes", view_menu)
        view_menu.addMenu(theme_menu)

        try:
            # Use rune-lib to discover all themes in the `themes` asset group
            discovered_themes = assets.themes.discover("*.scss")

            if not discovered_themes:
                raise AssetNotFoundError("No .scss files found in themes directory.", assets.themes, [])

            for theme_name in discovered_themes:
                action = QAction(theme_name, theme_menu)
                # Use a lambda to capture the current theme_name
                action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
                theme_menu.addAction(action)

        except (AttributeError, AssetNotFoundError):
            # This block runs if `assets.themes` doesn't exist or is empty
            action = QAction("No Themes Found", theme_menu)
            action.setEnabled(False)
            theme_menu.addAction(action)

    def apply_theme(self, theme_name: str):
        """Compiles a SASS file and applies it to the target widget."""
        try:
            # Use rune-lib to get the full path to the theme file
            scss_path = assets.themes.get(theme_name)
            if not scss_path or not scss_path.exists():
                raise FileNotFoundError

            # The rest of the logic remains the same
            include_paths = [str(scss_path.parent)]
            with open(scss_path, "r") as f:
                compiled_css = sass.compile(string=f.read(), include_paths=include_paths)
                self._target.setStyleSheet(compiled_css)

        except (AttributeError, FileNotFoundError):
            logging.warning(f"Theme '{theme_name}' not found. Applying the built-in default theme as a fallback.")
            self.apply_default_theme()
        except Exception as e:
            logging.error(f"Error applying theme {theme_name}: {e}")

    def apply_default_theme(self):
        """Applies the default theme bundled with qt-ingot."""
        try:
            # Access the bundled theme file content
            theme_content = pkg_resources.read_text('qt_ingot.resources.default_theme', 'theme.scss')
            colors_content = pkg_resources.read_text('qt_ingot.resources.default_theme', '_colors.scss')

            # Since sass.compile can't resolve @import from memory, we'll combine them
            full_scss = colors_content + "\n" + theme_content
            
            compiled_css = sass.compile(string=full_scss)
            self._target.setStyleSheet(compiled_css)
        except Exception as e:
            logging.error(f"Error applying default theme: {e}")