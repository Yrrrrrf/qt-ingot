"""
Simplified workspace for the camera-based system.
This replaces the complex multi-workspace setup with a single, unified approach.
"""

from PyQt6.QtWidgets import QTabWidget, QPushButton, QScrollArea
from PyQt6.QtCore import Qt
from .scene.view import SceneView
from .scene.manager import SceneManager


class SceneWorkspace(QTabWidget):
    """
    A tabbed workspace where each tab contains a SceneView.
    This is the unified workspace that replaces the previous multiple workspace types.
    """
    
    def __init__(self, update_slot=None):
        super().__init__()
        
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        
        # Add a "new tab" button to the corner
        add_button = QPushButton("+")
        add_button.setObjectName("ingotAddTabButton")
        add_button.clicked.connect(self.new_tab)
        self.setCornerWidget(add_button, Qt.Corner.TopRightCorner)
        
        # Store the update slot for status updates
        self._update_slot = update_slot
        
        # Start with one tab open
        self.new_tab()
    
    def new_tab(self):
        """Creates a new tab with a SceneView."""
        # Create a new scene manager for this tab
        scene_manager = SceneManager()
        
        # Create the SceneView with the scene manager
        scene_view = SceneView(scene_manager=scene_manager)
        
        # Connect the status updated signal if we have an update slot
        if self._update_slot:
            scene_view.status_updated.connect(self._update_slot)
        
        # Create a scroll area to wrap the scene view
        scroll_area = QScrollArea()
        scroll_area.setObjectName("ingotCanvasScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scene_view)
        
        # Set the cursor for the viewport to be a crosshair
        from PyQt6.QtGui import QCursor
        scroll_area.viewport().setCursor(QCursor(Qt.CursorShape.CrossCursor))
        
        # Add the scroll area as a new tab
        tab_number = self.count() + 1
        tab_text = f"Tab {tab_number}"
        index = self.addTab(scroll_area, tab_text)
        self.setCurrentIndex(index)
        
        # Center the view initially
        scene_view.center_on_position(0, 0)
        
        return scene_view
    
    def close_tab(self, index: int):
        """Closes the tab at the given index."""
        if self.count() > 1:
            self.removeTab(index)
        else:
            # Maybe show a message or prevent closing the last tab
            print("Cannot close the last tab.")
    
    def zoom_in(self):
        """Zoom in the current tab's scene view."""
        current_scroll_area = self.currentWidget()
        if current_scroll_area:
            scene_view = current_scroll_area.widget()
            if hasattr(scene_view, "zoom_in"):
                scene_view.zoom_in()
    
    def zoom_out(self):
        """Zoom out the current tab's scene view."""
        current_scroll_area = self.currentWidget()
        if current_scroll_area:
            scene_view = current_scroll_area.widget()
            if hasattr(scene_view, "zoom_out"):
                scene_view.zoom_out()
    
    def reset_zoom(self):
        """Reset zoom to 100% for the current tab's scene view."""
        current_scroll_area = self.currentWidget()
        if current_scroll_area:
            scene_view = current_scroll_area.widget()
            if hasattr(scene_view, "reset_zoom"):
                scene_view.reset_zoom()
    
    def toggle_scope(self):
        """Toggle the scope visibility on the current scene view."""
        current_scroll_area = self.currentWidget()
        if current_scroll_area:
            scene_view = current_scroll_area.widget()
            if hasattr(scene_view, "toggle_scope"):
                scene_view.toggle_scope()
