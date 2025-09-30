import sys
from PyQt6.QtWidgets import QApplication, QLabel

from rune import AssetNotFoundError, assets

from ingot.app import IngotApp
from ingot.views.base import BaseView


# --- Step 1: Define the application's custom view ---
# This remains the same. The developer provides the content for the tabs.
class MyTestView(BaseView):
    """A simple custom view that displays a label."""
    def __init__(self):
        super().__init__()
        label = QLabel("This is a custom view inside a new tab!\n\nClose this tab or press '+' to create another one.")
        label.setStyleSheet("font-size: 20px;")
        self.layout().addWidget(label)

# --- Step 2: Define the Application's Configuration ---
# Instead of setting the title and icon manually, we define a simple dictionary.
# `qt-ingot` will use this to configure the application window.
# The icon path is a `rune-lib` friendly path, which `IngotApp` will resolve.
APP_CONFIG = {
    "title": "My Awesome App",
    "version": "1.0.0",
    "author": "My Name",
    "icon": "img.template"  # A rune-lib friendly path
}


# --- Step 3: Define the Menu Structure ---
# MODIFIED to include a unique `id` for each action.
# This ID is used for registration in the ActionManager.



# --- Step 4: The Main Application Logic ---
def main():
    app = QApplication(sys.argv)

    # --- Use `qt-ingot` to build the window ---
    # We pass our view and the configuration dictionary to the IngotApp.
    # It handles the rest, including setting the title and icon.
    main_window = IngotApp(view_factory=MyTestView, config=APP_CONFIG)

    MENU_CONFIG = {
        "File": [
            {"id": "file.new_tab", "name": "New Tab", "shortcut": "T", "function": main_window.workspace.new_tab},
            {"id": "file.close_tab", "name": "Close Tab", "shortcut": "W", "function": lambda: main_window.workspace.close_tab(main_window.workspace.currentIndex())},
            {"id": "file.exit", "name": "Exit", "shortcut": "Esc", "function": sys.exit}
        ],
        "Help": [
            {"id": "help.about", "name": "About", "function": lambda: print("About This App!")}
        ]
    }

    # --- Set the Menu Bar ---
    # With the menu defined in a dictionary, we can set it with a single call.
    main_window.set_menu(MENU_CONFIG)

    # --- Add a Side Panel ---
    # The layout system allows adding widgets to the side.
    # Here, we add a simple label as a left-side panel.
    side_panel = QLabel("Side Panel")
    side_panel.setObjectName("sidePanel")
    main_window.set_side_panel(side_panel, position='left')

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
