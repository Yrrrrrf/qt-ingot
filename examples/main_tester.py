#!/usr/bin/env python3
"""
Simplified main tester for the refactored qt-ingot library.

This tester focuses on the core functionality:
- Basic scene with drawables
- Camera controls
- Status updates
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
    
    # Simple configuration
    config = {"title": "Qt-Ingot Main Tester"}
    
    # Create the application
    ingot_app = IngotApp(config=config)
    
    # Add content to the first tab
    current_tab = ingot_app.workspace.currentWidget()
    if current_tab:
        scene_view = current_tab.widget()
        if hasattr(scene_view, 'get_scene_manager'):
            scene_manager = scene_view.get_scene_manager()
            
            # Add basic shapes to test the functionality
            scene_manager.add_item(Rectangle(x=100, y=100, width=200, height=100, 
                                           color=QColor(100, 150, 200, 150)))
            scene_manager.add_item(Ellipse(x=350, y=150, width=150, height=150, 
                                         color=QColor(200, 100, 150, 150)))
            scene_manager.add_item(Text("Main Tester", x=200, y=350, 
                                      color=QColor(255, 255, 0), font_size=18))
    
    print("Qt-Ingot Main Tester launched!")
    print("Test functionality:")
    print("- Pan with middle mouse button or space+left click")
    print("- Zoom with mouse wheel or +/- keys")
    print("- Status bar shows position, zoom, and color under cursor")
    print("- Add more tabs with the + button")
    
    # Show the application
    ingot_app.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
