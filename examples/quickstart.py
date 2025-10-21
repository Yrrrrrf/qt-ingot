#!/usr/bin/env python3
"""
Quickstart example for the refactored qt-ingot library.

This demonstrates the simplest usage of the library.
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import the ingot module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor
from ingot.app import IngotApp
from ingot.scene.drawable import Rectangle, Ellipse, Text
from ingot.scene.manager import SceneManager


def main():
    app = QApplication(sys.argv)
    
    # Create the application with default configuration
    ingot_app = IngotApp()
    
    # Access the current scene and add a simple rectangle
    current_tab = ingot_app.workspace.currentWidget()
    if current_tab:
        scene_view = current_tab.widget()
        if hasattr(scene_view, 'get_scene_manager'):
            scene_manager = scene_view.get_scene_manager()
            
            # Add a simple rectangle to the scene
            scene_manager.add_item(Rectangle(
                x=100, y=100, 
                width=200, height=100, 
                color=QColor(100, 150, 200, 150)  # Semi-transparent blue
            ))
            scene_manager.add_item(Ellipse(
                x=300, y=200,
                width=150, height=150,
                color=QColor(200, 100, 150, 150)  # Semi-transparent pink
            ))
            scene_manager.add_item(Text(
                "Quick Start!", 
                x=200, y=350,
                color=QColor(255, 255, 255),  # White text
                font_size=20
            ))
    
    print("Qt-Ingot Quickstart launched!")
    print("Basic controls:")
    print("- Pan: Middle mouse or Space+Left drag")
    print("- Zoom: Mouse wheel or +/- keys")
    
    # Show the application
    ingot_app.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
