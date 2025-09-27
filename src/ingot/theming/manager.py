import sass
from pathlib import Path
import importlib.resources as pkg_resources
from PyQt6.QtWidgets import QWidget, QMenuBar, QMenu
from PyQt6.QtGui import QAction
import shutil
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ThemeManager:
    """Manages the loading, application, and scaffolding of SASS stylesheets."""
    def __init__(self, target_widget: QWidget, menu_bar: QMenuBar, user_themes_path: str | Path = "resources/themes"):
        self._target = target_widget
        self._menu_bar = menu_bar
        self._user_themes_path = Path(user_themes_path)
        self._scaffold_user_theme()
        self._discover_and_add_themes_to_menu()

    def _scaffold_user_theme(self):
        """
        Checks if the user's theme directory exists. If not, it creates a
        default theme setup for them.
        """
        theme_file = self._user_themes_path / "theme.scss"
        colors_file = self._user_themes_path / "_colors.scss"

        if theme_file.exists() and colors_file.exists():
            return # Theme files already exist

        logging.info("User 'themes' directory not found or incomplete. Creating a default setup...")
        
        try:
            self._user_themes_path.mkdir(parents=True, exist_ok=True)

            # Copy the default theme files from the package resources
            with pkg_resources.path('qt_ingot.resources.default_theme', 'theme.scss') as src_theme:
                shutil.copy(src_theme, theme_file)
            
            with pkg_resources.path('qt_ingot.resources.default_theme', '_colors.scss') as src_colors:
                shutil.copy(src_colors, colors_file)

            logging.info(f"SUCCESS: A default theme has been created at '{self._user_themes_path}'.")

        except Exception as e:
            logging.error(f"Failed to create default theme: {e}")

    def _discover_and_add_themes_to_menu(self):
        """Discovers .scss themes and adds them to the 'View' menu."""
        view_menu = self._menu_bar.findChild(QMenu, "View")
        if not view_menu:
            view_menu = QMenu("View", self._menu_bar)
            self._menu_bar.addMenu(view_menu)

        theme_menu = QMenu("Themes", view_menu)
        view_menu.addMenu(theme_menu)

        theme_files = list(self._user_themes_path.glob("*.scss"))
        if not theme_files:
            action = QAction("No Themes Found", theme_menu)
            action.setEnabled(False)
            theme_menu.addAction(action)
            return

        for theme_path in theme_files:
            theme_name = theme_path.stem
            action = QAction(theme_name, theme_menu)
            action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(action)

    def apply_theme(self, theme_name: str):
        """Compiles a SASS file and applies it to the target widget."""
        scss_path = self._user_themes_path / f"{theme_name}.scss"
        if not scss_path.exists():
            logging.warning(f"Theme '{theme_name}' not found. Applying the built-in default theme as a fallback.")
            self.apply_default_theme()
            return

        try:
            # Define include paths for @import rules, like for _colors.scss
            include_paths = [str(scss_path.parent)]
            
            with open(scss_path, "r") as f:
                compiled_css = sass.compile(string=f.read(), include_paths=include_paths)
                self._target.setStyleSheet(compiled_css)
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