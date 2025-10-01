import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from rune import AssetNotFoundError, assets

from ingot.app import IngotApp
from ingot.views.base import BaseView

# Simple view for standard workspace
class MyTestView(BaseView):
    """A simple custom view that displays a label."""
    def __init__(self):
        super().__init__()
        label = QLabel("This is a simple test view!\n\nClose this tab or press '+' to create another one.")
        label.setStyleSheet("font-size: 16px;")
        self.layout().addWidget(label)


# --- Application Configuration ---
APP_CONFIG = {
    "title": "Qt Ingot - Simple Test",
    "version": "1.3.0",
    "author": "My Name",
    "icon": "img.template"  # A rune-lib friendly path
}

# --- View Configuration for the Workspace ---
# Use simple view for standard workspace
VIEW_CONFIG = {
    "view_factory": MyTestView,
}


# --- Helper functions for new menu actions ---
current_app_instance = None # Global variable to hold the main window instance for actions
# Track panel visibility state
left_panel_visible = True
right_panel_visible = True

def exit_app():
    """Exit the application."""
    sys.exit()

def toggle_side_panel(position: str):
    """Toggles the visibility of the specified side panel."""
    global current_app_instance, left_panel_visible, right_panel_visible
    if current_app_instance:
        # Access the display object which manages the side panels
        display_widget = current_app_instance.display # This is the Display instance
        # Find the side panel widget based on position
        # The object name was set in Phase 1: f"ingotSidePanel_{position}"
        panel_widget = current_app_instance.findChild(QWidget, f"ingotSidePanel_{position}")
        if panel_widget:
            # Toggle visibility based on current state and update tracking variable
            if position == 'left':
                left_panel_visible = not left_panel_visible
                panel_widget.setVisible(left_panel_visible)
            elif position == 'right':
                right_panel_visible = not right_panel_visible
                panel_widget.setVisible(right_panel_visible)
            print(f"Toggled {position} panel visibility: {panel_widget.isVisible()}")
        else:
            print(f"Side panel for position '{position}' not found (object name 'ingotSidePanel_{position}').")

# --- Define the Menu Structure with IDs and New Actions ---
MENU_CONFIG = {
    "File": [
        {"id": "file.new_tab", "name": "New Tab", "shortcut": "Ctrl+T", "function": lambda: current_app_instance.workspace.new_tab() if current_app_instance else None}, # Example: Use lambda to capture main_window later
        {"id": "file.close_tab", "name": "Close Tab", "shortcut": "Ctrl+W", "function": lambda: current_app_instance.workspace.close_tab(current_app_instance.workspace.currentIndex()) if current_app_instance else None}, # Example: Use lambda
        {"id": "file.exit", "name": "Exit", "shortcut": "Ctrl+Q", "function": exit_app}
    ],
    "View": [
        # Add separator and panel toggling actions
        {"separator": True},
        {"id": "view.toggle_left_panel", "name": "Toggle Left Panel", "shortcut": "Ctrl+L", "function": lambda: toggle_side_panel('left')},
        {"id": "view.toggle_right_panel", "name": "Toggle Right Panel", "shortcut": "Ctrl+R", "function": lambda: toggle_side_panel('right')},
    ],
    "Help": [
        {"id": "help.about", "name": "About", "function": lambda: print("Qt Ingot Simple Test v1.3.0!")}
    ]
}


# --- The Main Application Logic ---
def main():
    app = QApplication(sys.argv)

    # --- Use `qt-ingot` to build the window ---
    # Use the standard configuration by default
    workspace_type_to_use = "standard"
    main_window = IngotApp(view_config=VIEW_CONFIG, config=APP_CONFIG, workspace_type=workspace_type_to_use)

    # Assign the main window instance to the global variable for menu actions
    global current_app_instance
    current_app_instance = main_window

    # --- Set the Menu Bar ---
    main_window.set_menu(MENU_CONFIG)

    # --- Add Left Side Panel ---
    # The layout system allows adding widgets to the side.
    # The new naming from Phase 1 allows specific styling in theme.scss
    left_panel = QLabel("Left Panel\n(Demonstrates\nObject Naming)\n\nPress Ctrl+L to toggle me!")
    # Note: The setObjectName will now happen automatically inside main_window.set_side_panel
    # due to the changes in Phase 1. The theme.scss targets ingotSidePanel_left/right.
    main_window.set_side_panel(left_panel, position='left')
    
    # --- Add Right Side Panel ---
    right_panel = QLabel("Right Panel\n(Demonstrates\nObject Naming)\n\nPress Ctrl+R to toggle me!")
    main_window.set_side_panel(right_panel, position='right')

    main_window.show()
    
    # Add shortcut for ESC to exit
    from PyQt6.QtGui import QKeySequence, QShortcut
    shortcut = QShortcut(QKeySequence("Escape"), main_window)
    shortcut.activated.connect(sys.exit)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()