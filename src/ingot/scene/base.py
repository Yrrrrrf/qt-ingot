"""
Base classes for scene management in the camera-based system.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QPointF
from typing import List, Optional


class SceneBase(QObject):
    """
    Base class for scenes that can contain SceneItems.
    Defines the interface for scene management.
    """
    
    # Signal emitted when the scene content changes
    scene_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def get_items(self) -> List['SceneItem']:
        """
        Get all items in the scene.
        
        Returns:
            List of SceneItem objects
        """
        raise NotImplementedError("Subclasses must implement get_items()")
    
    def add_item(self, item: 'SceneItem'):
        """
        Add an item to the scene.
        
        Args:
            item: SceneItem to add
        """
        raise NotImplementedError("Subclasses must implement add_item()")
    
    def remove_item(self, item: 'SceneItem'):
        """
        Remove an item from the scene.
        
        Args:
            item: SceneItem to remove
        """
        raise NotImplementedError("Subclasses must implement remove_item()")
    
    def clear_items(self):
        """Remove all items from the scene."""
        raise NotImplementedError("Subclasses must implement clear_items()")


class SceneItem(QObject):
    """
    Base class for items that can be rendered in a scene.
    """
    
    # Signal emitted when the item properties change
    item_changed = pyqtSignal()
    
    def __init__(self, x: float = 0, y: float = 0, z_index: int = 0, visible: bool = True, locked: bool = False):
        super().__init__()
        
        # Position in scene coordinates
        self._pos = QPointF(x, y)
        self._z_index = z_index  # Rendering order (higher z_index renders on top)
        self._visible = visible
        self._locked = locked  # If locked, the item can't be interacted with
    
    @property
    def x(self) -> float:
        """Get the X coordinate of the item."""
        return self._pos.x()
    
    @x.setter
    def x(self, value: float):
        """Set the X coordinate of the item."""
        self._pos.setX(value)
        self.item_changed.emit()
    
    @property
    def y(self) -> float:
        """Get the Y coordinate of the item."""
        return self._pos.y()
    
    @y.setter
    def y(self, value: float):
        """Set the Y coordinate of the item."""
        self._pos.setY(value)
        self.item_changed.emit()
    
    @property
    def z_index(self) -> int:
        """Get the Z index (rendering order) of the item."""
        return self._z_index
    
    @z_index.setter
    def z_index(self, value: int):
        """Set the Z index (rendering order) of the item."""
        self._z_index = value
        self.item_changed.emit()
    
    @property
    def visible(self) -> bool:
        """Get whether the item is visible."""
        return self._visible
    
    @visible.setter
    def visible(self, value: bool):
        """Set whether the item is visible."""
        self._visible = value
        self.item_changed.emit()
    
    @property
    def locked(self) -> bool:
        """Get whether the item is locked."""
        return self._locked
    
    @locked.setter
    def locked(self, value: bool):
        """Set whether the item is locked."""
        self._locked = value
        self.item_changed.emit()
    
    def get_position(self) -> QPointF:
        """
        Get the position of the item in scene coordinates.
        
        Returns:
            QPointF position of the item
        """
        return self._pos
    
    def set_position(self, pos: QPointF):
        """
        Set the position of the item in scene coordinates.
        
        Args:
            pos: New position of the item
        """
        self._pos = pos
        self.item_changed.emit()
    
    def get_center_position(self) -> QPointF:
        """
        Get the center position of the item in scene coordinates.
        
        Returns:
            QPointF center position of the item (default to position if no size information)
        """
        return self._pos
    
    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the item contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
            
        Returns:
            True if the item contains the point, False otherwise
        """
        # Default implementation - subclasses should override based on their shape
        # For now, just check if the point is very close to the item's position
        distance = ((point.x() - self._pos.x()) ** 2 + (point.y() - self._pos.y()) ** 2) ** 0.5
        return distance < 10  # Default threshold of 10 pixels
    
    def paint(self, painter: QPainter):
        """
        Paint the scene item using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the item
        """
        raise NotImplementedError("Subclasses must implement paint()")
    
    def on_clicked(self, point: QPointF):
        """
        Handle click events on the item.
        
        Args:
            point: Point in scene coordinates where the click occurred
        """
        # Default implementation does nothing - subclasses can override
        pass
