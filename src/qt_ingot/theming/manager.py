import sass
from pathlib import Path
import importlib.resources as pkg_resources
from PyQt6.QtWidgets import QWidget
import shutil
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ThemeManager:
    """Manages the loading, application, and scaffolding of SASS stylesheets."""
    def __init__(self, target_widget: QWidget, user_themes_path: str | Path = "resources/themes"):
        self._target = target_widget
        self._user_themes_path = Path(user_themes_path)
        self._scaffold_user_theme()

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

    def apply_theme(self, scss_path: str | Path):
        """Compiles a SASS file and applies it to the target widget."""
        try:
            scss_path = Path(scss_path)
            # Define include paths for @import rules, like for _colors.scss
            include_paths = [str(scss_path.parent)]
            
            with open(scss_path, "r") as f:
                compiled_css = sass.compile(string=f.read(), include_paths=include_paths)
                self._target.setStyleSheet(compiled_css)
        except FileNotFoundError:
            logging.warning(f"Theme '{scss_path.name}' not found. Applying the built-in default theme as a fallback.")
            self.apply_default_theme()
        except Exception as e:
            logging.error(f"Error applying theme {scss_path}: {e}")

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