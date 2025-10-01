import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt

from rune import AssetNotFoundError, assets

from ingot.app import IngotApp
from ingot.views.base import BaseView
# Import the new layout structures
from ingot.layouts import HSplit, VSplit, Leaf

# --- Simple widget for canvas ---
class CanvasContent(QWidget):
    """A simple widget that could represent content in a canvas, suitable for zooming."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Canvas Content Area")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add a simple graphic element
        scene = QGraphicsScene()
        rect = QGraphicsRectItem(0, 0, 800, 600)  # Larger scene to test scrolling
        rect.setFlag(rect.GraphicsItemFlag.ItemIsMovable)
        scene.addItem(rect)
        view = QGraphicsView(scene)
        view.setRenderHint(view.RenderHint.Antialiasing)
        layout.addWidget(view)

        self.setLayout(layout)

    # Interface for zooming (if CanvasWorkspace attempts to use it)
    def scale(self, sx, sy):
        # Find the QGraphicsView child and scale it
        view = self.findChild(QGraphicsView)
        if view:
             view.scale(sx, sy)

    def reset_scale(self):
        # Find the QGraphicsView child and reset its transform
        view = self.findChild(QGraphicsView)
        if view:
             view.resetTransform()

# Simple view for standard workspace
class MyTestView(BaseView):
    """A simple custom view that displays a label."""
    def __init__(self):
        super().__init__()
        label = QLabel("This is a simple test view!\n\nYou can switch to canvas workspace to test scrolling and zooming.")
        label.setStyleSheet("font-size: 16px;")
        self.layout().addWidget(label)


# --- Application Configuration ---
APP_CONFIG = {
    "title": "Qt Ingot - Simple Test",
    "version": "1.2.0",
    "author": "My Name",
    "icon": "img.template"  # A rune-lib friendly path
}

# --- View Configuration for the Workspace ---
# Use simple view for standard workspace
VIEW_CONFIG = {
    "view_factory": MyTestView,
}

# View config for canvas workspace
CANVAS_VIEW_CONFIG = {
    "view_factory": CanvasContent,
}


# --- Helper functions for new menu actions ---
current_app_instance = None # Global variable to hold the main window instance for actions
# Track panel visibility state
left_panel_visible = True
right_panel_visible = True

def switch_to_canvas_workspace():
    """Switch to canvas workspace."""
    global current_app_instance
    if current_app_instance:
        print("Switching to canvas workspace...")
        # Create a new instance with canvas workspace type
        # For simplicity in this example, we'll use a message
        print("Canvas workspace selected. Canvas content will be shown in new tabs.")

def switch_to_standard_workspace():
    """Switch to standard workspace."""
    global current_app_instance
    if current_app_instance:
        print("Switching to standard workspace...")
        print("Standard workspace selected. Standard content will be shown in new tabs.")

def zoom_canvas(factor: float):
    """Attempts to zoom the canvas content."""
    global current_app_instance
    if current_app_instance and hasattr(current_app_instance, 'workspace'):
        # Check if the current workspace is a CanvasWorkspace (it has zoom methods)
        if hasattr(current_app_instance.workspace, 'zoom_in'):
             if factor > 1.0:
                 current_app_instance.workspace.zoom_in(factor)
             else:
                 current_app_instance.workspace.zoom_out(1.0 / (1.0 / factor))
        else:
            print("Zoom action ignored: Current workspace does not support zooming.")
    else:
        print("Zoom action failed: Canvas workspace or zoom methods not found.")

def reset_canvas_zoom():
    """Attempts to reset the canvas zoom level."""
    global current_app_instance
    if current_app_instance and hasattr(current_app_instance, 'workspace'):
        # Check if the current workspace is a CanvasWorkspace (it has reset_zoom method)
        if hasattr(current_app_instance.workspace, 'reset_zoom'):
             current_app_instance.workspace.reset_zoom()
        else:
            print("Reset Zoom action ignored: Current workspace does not support zooming.")
    else:
        print("Reset Zoom action failed: Canvas workspace or reset method not found.")

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
        {"id": "file.exit", "name": "Exit", "shortcut": "Ctrl+Q", "function": sys.exit}
    ],
    "View": [
        # Add submenu for workspace type selection
        {"id": "view.workspace_standard", "name": "Standard Workspace", "function": lambda: switch_to_standard_workspace()},
        {"id": "view.workspace_canvas", "name": "Canvas Workspace", "function": lambda: switch_to_canvas_workspace()},
        # Add separator and zoom actions (only active if canvas workspace is active)
        {"separator": True},
        {"id": "view.zoom_in", "name": "Zoom In (Canvas)", "shortcut": "Ctrl+=", "function": lambda: zoom_canvas(1.2)},
        {"id": "view.zoom_out", "name": "Zoom Out (Canvas)", "shortcut": "Ctrl+-", "function": lambda: zoom_canvas(0.8)},
        {"id": "view.reset_zoom", "name": "Reset Zoom (Canvas)", "shortcut": "Ctrl+0", "function": lambda: reset_canvas_zoom()},
        # Add separator and panel toggling actions
        {"separator": True},
        {"id": "view.toggle_left_panel", "name": "Toggle Left Panel", "shortcut": "Ctrl+L", "function": lambda: toggle_side_panel('left')},
        {"id": "view.toggle_right_panel", "name": "Toggle Right Panel", "shortcut": "Ctrl+R", "function": lambda: toggle_side_panel('right')},
    ],
    "Help": [
        {"id": "help.about", "name": "About", "function": lambda: print("Qt Ingot Simple Test v1.2.0!")}
    ]
}


# --- The Main Application Logic ---
def main():
    app = QApplication(sys.argv)

    # --- CHOOSE WORKSPACE TYPE ---
    # Default to standard for basic testing
    workspace_type_to_use = "standard" # Change to "canvas" to test canvas directly

    # --- Use `qt-ingot` to build the window ---
    # Use the standard configuration by default
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
    sys.exit(app.exec())


if __name__ == "__main__":
    main()