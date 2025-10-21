"""
Scene item implementations for the camera-based scene system.
"""

from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtCore import QRectF, QPointF
from .base import SceneItem


class RectangleItem(SceneItem):
    """
    A rectangle scene item that can be rendered in the scene.
    """
    
    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                 color: QColor = None, z_index: int = 0, visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)
        
        self._width = width
        self._height = height
        self._color = color or QColor(100, 150, 200, 150)  # Default semi-transparent blue
        self._border_color = QColor(200, 200, 200)  # Default light gray border
    
    @property
    def width(self) -> float:
        """Get the width of the rectangle."""
        return self._width
    
    @width.setter
    def width(self, value: float):
        """Set the width of the rectangle."""
        self._width = value
        self.item_changed.emit()
    
    @property
    def height(self) -> float:
        """Get the height of the rectangle."""
        return self._height
    
    @height.setter
    def height(self, value: float):
        """Set the height of the rectangle."""
        self._height = value
        self.item_changed.emit()
    
    @property
    def color(self) -> QColor:
        """Get the fill color of the rectangle."""
        return self._color
    
    @color.setter
    def color(self, value: QColor):
        """Set the fill color of the rectangle."""
        self._color = value
        self.item_changed.emit()
    
    def get_center_position(self) -> QPointF:
        """
        Get the center position of the rectangle in scene coordinates.
        
        Returns:
            QPointF center position of the rectangle
        """
        return QPointF(self._pos.x() + self._width / 2, self._pos.y() + self._height / 2)
    
    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the rectangle contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
            
        Returns:
            True if the rectangle contains the point, False otherwise
        """
        return (self._pos.x() <= point.x() <= self._pos.x() + self._width and
                self._pos.y() <= point.y() <= self._pos.y() + self._height)
    
    def paint(self, painter: QPainter):
        """
        Paint the rectangle using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the rectangle
        """
        if not self._visible:
            return
            
        # Save the painter state
        painter.save()
        
        # Set pen and brush for drawing
        pen = QPen(self._border_color, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self._color))
        
        # Draw the rectangle
        rect = QRectF(self._pos.x(), self._pos.y(), self._width, self._height)
        painter.drawRect(rect)
        
        # Restore the painter state
        painter.restore()


class EllipseItem(SceneItem):
    """
    An ellipse scene item that can be rendered in the scene.
    """
    
    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                 color: QColor = None, z_index: int = 0, visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)
        
        self._width = width
        self._height = height
        self._color = color or QColor(200, 100, 150, 150)  # Default semi-transparent pink
        self._border_color = QColor(200, 200, 200)  # Default light gray border
    
    @property
    def width(self) -> float:
        """Get the width of the ellipse."""
        return self._width
    
    @width.setter
    def width(self, value: float):
        """Set the width of the ellipse."""
        self._width = value
        self.item_changed.emit()
    
    @property
    def height(self) -> float:
        """Get the height of the ellipse."""
        return self._height
    
    @height.setter
    def height(self, value: float):
        """Set the height of the ellipse."""
        self._height = value
        self.item_changed.emit()
    
    @property
    def color(self) -> QColor:
        """Get the fill color of the ellipse."""
        return self._color
    
    @color.setter
    def color(self, value: QColor):
        """Set the fill color of the ellipse."""
        self._color = value
        self.item_changed.emit()
    
    def get_center_position(self) -> QPointF:
        """
        Get the center position of the ellipse in scene coordinates.
        
        Returns:
            QPointF center position of the ellipse
        """
        return QPointF(self._pos.x() + self._width / 2, self._pos.y() + self._height / 2)
    
    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the ellipse contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
            
        Returns:
            True if the ellipse contains the point, False otherwise
        """
        # Translate point to ellipse coordinate system
        centered_x = point.x() - (self._pos.x() + self._width / 2)
        centered_y = point.y() - (self._pos.y() + self._height / 2)
        
        # Check if point is inside ellipse
        # Ellipse formula: (x^2 / a^2) + (y^2 / b^2) <= 1
        a = self._width / 2
        b = self._height / 2
        
        return (centered_x ** 2) / (a ** 2) + (centered_y ** 2) / (b ** 2) <= 1
    
    def paint(self, painter: QPainter):
        """
        Paint the ellipse using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the ellipse
        """
        if not self._visible:
            return
            
        # Save the painter state
        painter.save()
        
        # Set pen and brush for drawing
        pen = QPen(self._border_color, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self._color))
        
        # Draw the ellipse
        rect = QRectF(self._pos.x(), self._pos.y(), self._width, self._height)
        painter.drawEllipse(rect)
        
        # Restore the painter state
        painter.restore()


class TextItem(SceneItem):
    """
    A text scene item that can be rendered in the scene.
    """
    
    def __init__(self, text: str, x: float = 0, y: float = 0, 
                 font_size: int = 12, color: QColor = None, 
                 z_index: int = 0, visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)
        
        self._text = text
        self._font_size = font_size
        self._color = color or QColor(255, 255, 255)  # Default white text
        self._font = QFont()
        self._font.setPointSize(self._font_size)
    
    @property
    def text(self) -> str:
        """Get the text content."""
        return self._text
    
    @text.setter
    def text(self, value: str):
        """Set the text content."""
        self._text = value
        self.item_changed.emit()
    
    @property
    def font_size(self) -> int:
        """Get the font size."""
        return self._font_size
    
    @font_size.setter
    def font_size(self, value: int):
        """Set the font size."""
        self._font_size = value
        self._font.setPointSize(value)
        self.item_changed.emit()
    
    @property
    def color(self) -> QColor:
        """Get the text color."""
        return self._color
    
    @color.setter
    def color(self, value: QColor):
        """Set the text color."""
        self._color = value
        self.item_changed.emit()
    
    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the text item contains the given scene point.
        For simplicity, we'll use a bounding box approximation.
        
        Args:
            point: Point in scene coordinates to check
            
        Returns:
            True if the text contains the point, False otherwise
        """
        # This is a simple approximation - for more precision, we'd need to 
        # calculate the actual text bounds using QFontMetrics
        # For now, we'll use a 100x20 bounding box around the position
        return (self._pos.x() <= point.x() <= self._pos.x() + 100 and
                self._pos.y() <= point.y() <= self._pos.y() + 20)
    
    def paint(self, painter: QPainter):
        """
        Paint the text using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the text
        """
        if not self._visible:
            return
            
        # Save the painter state
        painter.save()
        
        # Set font and color
        painter.setFont(self._font)
        painter.setPen(self._color)
        
        # Draw the text
        painter.drawText(self._pos, self._text)
        
        # Restore the painter state
        painter.restore()

    def get_center_position(self) -> QPointF:
        """
        Get the center position of the text in scene coordinates.
        For simplicity, we'll return the starting position.
        A more accurate implementation would use QFontMetrics to find the center.
        
        Returns:
            QPointF center position of the text
        """
        return self._pos
