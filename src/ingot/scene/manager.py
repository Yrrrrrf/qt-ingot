"""
Scene manager for the camera-based system.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from typing import List
from .drawable import Drawable


class SceneManager(QObject):
    """
    Manages a scene containing multiple Drawable items.
    """
    
    # Signal emitted when scene items are added, removed, or changed
    items_changed = pyqtSignal()
    scene_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # List of items in the scene
        self._items: List[Drawable] = []
        
        # Connect item change signals to update the scene
        self._items_changed = False
    
    def get_items(self) -> List[Drawable]:
        """
        Get all items in the scene.
        
        Returns:
            List of Drawable objects
        """
        # Sort items by z_index to ensure correct drawing order before returning
        sorted_items = sorted(self._items, key=lambda x: x.z_index)
        return sorted_items  # Return items in drawing order
    
    def add_item(self, item: Drawable):
        """
        Add an item to the scene.
        
        Args:
            item: Drawable to add
        """
        self._items.append(item)
        # Sort items by z_index to ensure correct drawing order
        self._items.sort(key=lambda x: x.z_index)
        
        self._items_changed = True
        self.items_changed.emit()
        self.scene_changed.emit()
    
    def remove_item(self, item: Drawable):
        """
        Remove an item from the scene.
        
        Args:
            item: Drawable to remove
        """
        if item in self._items:
            self._items.remove(item)
            
            self._items_changed = True
            self.items_changed.emit()
            self.scene_changed.emit()
    
    def clear_items(self):
        """Remove all items from the scene."""
        self._items.clear()
        self._items_changed = True
        self.items_changed.emit()
        self.scene_changed.emit()
    
    def get_item_at_position(self, pos) -> Drawable:
        """
        Find the topmost item at the given position.
        
        Args:
            pos: Position in scene coordinates
        
        Returns:
            The topmost Drawable at the position, or None if no item is found
        """
        # Check items in reverse order (top to bottom) to find the topmost item
        for item in reversed(self._items):
            if hasattr(item, 'visible') and item.visible and hasattr(item, 'locked') and not item.locked:
                if hasattr(item, 'contains_point') and item.contains_point(pos):
                    return item
        return None
    
    def get_items_in_rect(self, x: float, y: float, width: float, height: float) -> List[Drawable]:
        """
        Find all items that intersect with the given rectangle.
        
        Args:
            x, y: Top-left corner of the rectangle
            width, height: Size of the rectangle
        
        Returns:
            List of Drawables that intersect with the rectangle
        """
        result = []
        rect_x1, rect_y1 = x, y
        rect_x2, rect_y2 = x + width, y + height
        
        for item in self._items:
            if hasattr(item, 'visible') and item.visible and hasattr(item, 'locked') and not item.locked:
                item_x = getattr(item, 'x', 0)
                item_y = getattr(item, 'y', 0)
                
                # This is a simple point-based check - a more sophisticated 
                # implementation would check actual item bounds
                if rect_x1 <= item_x <= rect_x2 and rect_y1 <= item_y <= rect_y2:
                    result.append(item)
        
        return result
