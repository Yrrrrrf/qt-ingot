#!/usr/bin/env python3
"""
Showcase of the refactored qt-ingot library with all features demonstrated.

This example shows:
- Camera-based scene with pan/zoom functionality
- Multiple drawable types (Rectangle, Ellipse, Text)
- Crosshair and status updates
- Tabbed workspace
- Color sampling and position tracking
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import the ingot module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ingot.app import IngotApp
from ingot.scene.drawable import Rectangle, Ellipse, Text, WidgetWrapper
from ingot.scene.manager import SceneManager


def main():
    app = QApplication(sys.argv)
    
    # Create a simple configuration
    config = {
        "title": "Qt-Ingot Feature Showcase",
    }
    
    # Create the application with the new unified architecture
    ingot_app = IngotApp(config=config)
    
    # Add some sample content to the first tab
    current_tab = ingot_app.workspace.currentWidget()
    if current_tab:
        scene_view = current_tab.widget()  # This is the SceneView wrapped in QScrollArea
        if hasattr(scene_view, 'get_scene_manager'):
            scene_manager = scene_view.get_scene_manager()
            
            # Add various drawable items to demonstrate the features
            scene_manager.add_item(Rectangle(
                x=100, y=100, 
                width=200, height=100, 
                color=QColor(100, 150, 200, 150),  # Semi-transparent blue
                z_index=0
            ))
            scene_manager.add_item(Ellipse(
                x=350, y=150, 
                width=150, height=150, 
                color=QColor(200, 100, 150, 150),  # Semi-transparent pink
                z_index=1
            ))
            scene_manager.add_item(Text(
                "Sample Text", 
                x=200, y=350, 
                color=QColor(255, 255, 0),  # Yellow text
                font_size=16,
                z_index=2
            ))
            scene_manager.add_item(Rectangle(
                x=500, y=300, 
                width=120, height=80, 
                color=QColor(50, 200, 100, 150),  # Semi-transparent green
                z_index=3
            ))
    
    # Add a second tab to demonstrate tab functionality
    ingot_app.workspace.new_tab()
    second_tab = ingot_app.workspace.widget(1)
    if second_tab:
        scene_view = second_tab.widget()
        if hasattr(scene_view, 'get_scene_manager'):
            scene_manager = scene_view.get_scene_manager()
            
            # Add different content to the second tab
            scene_manager.add_item(Rectangle(
                x=-50, y=-50, 
                width=400, height=300, 
                color=QColor(150, 100, 200, 120),  # Purple
                z_index=0
            ))
            scene_manager.add_item(Ellipse(
                x=200, y=100, 
                width=200, height=200, 
                color=QColor(255, 165, 0, 150),  # Orange
                z_index=1
            ))
            scene_manager.add_item(Text(
                "Second Tab", 
                x=100, y=250, 
                color=QColor(0, 255, 255),  # Cyan text
                font_size=20,
                z_index=2
            ))
    
    # Create a side panel widget to demonstrate that feature
    side_panel = QWidget()
    side_panel_layout = QVBoxLayout()
    
    label = QLabel("Qt-Ingot Showcase\nControls:")
    label.setWordWrap(True)
    
    pan_label = QLabel("• Pan: Middle mouse or Space+Left drag")
    zoom_label = QLabel("• Zoom: Mouse wheel or +/- keys")
    reset_label = QLabel("• Reset: 0 key")
    home_label = QLabel("• Center: Home/H key")
    scope_label = QLabel("• Toggle scope: Ctrl+T (if implemented in menu)")
    
    side_panel_layout.addWidget(label)
    side_panel_layout.addWidget(pan_label)
    side_panel_layout.addWidget(zoom_label)
    side_panel_layout.addWidget(reset_label)
    side_panel_layout.addWidget(home_label)
    side_panel_layout.addWidget(scope_label)
    side_panel_layout.addStretch()  # Push items to the top
    
    side_panel.setLayout(side_panel_layout)
    
    # Add the side panel to the application
    ingot_app.set_side_panel(side_panel, "left")
    
    # Show the application
    ingot_app.show()
    
    print("Qt-Ingot Feature Showcase launched!")
    print("Features demonstrated:")
    print("- Camera-based infinite canvas with pan/zoom")
    print("- Multiple drawable types: Rectangle, Ellipse, Text")
    print("- Crosshair cursor that follows mouse")
    print("- Status bar updates (position, zoom, color)")
    print("- Tabbed workspace with multiple scenes")
    print("- Zoom-to-cursor functionality")
    print("- Keyboard controls for navigation")
    print("- Side panel integration")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
