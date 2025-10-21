"""
Drawable classes for the SceneView architecture.

This combines the previous drawable.py and item.py functionality into a single, cohesive module.
"""
from abc import ABC, abstractmethod
from PyQt6.QtCore import QPoint, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont


class Drawable(ABC):
    """
    Abstract base class for all drawable items in the SceneView.
    
    This class defines the interface that all scene objects must implement.
    """

    def __init__(self, x: float = 0, y: float = 0, z_index: int = 0, visible: bool = True, locked: bool = False):
        """
        Initialize the drawable item.
        
        Args:
            x: X coordinate in scene space
            y: Y coordinate in scene space  
            z_index: The drawing order index (higher values are drawn on top)
            visible: Whether the item should be rendered
            locked: Whether the item is locked from interaction
        """
        self.x = x
        self.y = y
        self.z_index = z_index
        self.visible = visible
        self.locked = locked

    @abstractmethod
    def paint(self, painter: QPainter) -> None:
        """
        Draw the item using the provided painter.
        
        Args:
            painter: The QPainter to use for drawing
        """
        pass

    @abstractmethod
    def get_bounding_box(self) -> QRectF:
        """
        Get the bounding box of the drawable item.
        
        Returns:
            QRectF representing the bounding box of the item
        """
        pass

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
        distance = ((point.x() - self.x) ** 2 + (point.y() - self.y) ** 2) ** 0.5
        return distance < 10  # Default threshold of 10 pixels

    def on_clicked(self, point: QPointF):
        """
        Handle click events on the item.
        
        Args:
            point: Point in scene coordinates where the click occurred
        """
        # Default implementation does nothing - subclasses can override
        pass


class Rectangle(Drawable):
    """
    A rectangle drawable that can be rendered in the scene.
    """

    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                 color: QColor = None, border_color: QColor = None, z_index: int = 0, 
                 visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)

        self.width = width
        self.height = height
        self.color = color or QColor(100, 150, 200, 150)  # Default semi-transparent blue
        self.border_color = border_color or QColor(200, 200, 200)  # Default light gray border

    def get_bounding_box(self) -> QRectF:
        """Get the bounding box of the rectangle."""
        return QRectF(self.x, self.y, self.width, self.height)

    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the rectangle contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
        
        Returns:
            True if the rectangle contains the point, False otherwise
        """
        return (self.x <= point.x() <= self.x + self.width and
                self.y <= point.y() <= self.y + self.height)

    def paint(self, painter: QPainter):
        """
        Paint the rectangle using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the rectangle
        """
        if not self.visible:
            return

        # Save the painter state
        painter.save()

        # Set pen and brush for drawing
        pen = QPen(self.border_color, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self.color))

        # Draw the rectangle
        rect = QRectF(self.x, self.y, self.width, self.height)
        painter.drawRect(rect)

        # Restore the painter state
        painter.restore()


class Ellipse(Drawable):
    """
    An ellipse drawable that can be rendered in the scene.
    """

    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                 color: QColor = None, border_color: QColor = None, z_index: int = 0, 
                 visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)

        self.width = width
        self.height = height
        self.color = color or QColor(200, 100, 150, 150)  # Default semi-transparent pink
        self.border_color = border_color or QColor(200, 200, 200)  # Default light gray border

    def get_bounding_box(self) -> QRectF:
        """Get the bounding box of the ellipse."""
        return QRectF(self.x, self.y, self.width, self.height)

    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the ellipse contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
        
        Returns:
            True if the ellipse contains the point, False otherwise
        """
        # Translate point to ellipse coordinate system
        centered_x = point.x() - (self.x + self.width / 2)
        centered_y = point.y() - (self.y + self.height / 2)

        # Check if point is inside ellipse
        # Ellipse formula: (x^2 / a^2) + (y^2 / b^2) <= 1
        a = self.width / 2
        b = self.height / 2

        return (centered_x ** 2) / (a ** 2) + (centered_y ** 2) / (b ** 2) <= 1

    def paint(self, painter: QPainter):
        """
        Paint the ellipse using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the ellipse
        """
        if not self.visible:
            return

        # Save the painter state
        painter.save()

        # Set pen and brush for drawing
        pen = QPen(self.border_color, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self.color))

        # Draw the ellipse
        rect = QRectF(self.x, self.y, self.width, self.height)
        painter.drawEllipse(rect)

        # Restore the painter state
        painter.restore()


class Text(Drawable):
    """
    A text drawable that can be rendered in the scene.
    """

    def __init__(self, text: str, x: float = 0, y: float = 0,
                 font_size: int = 12, color: QColor = None,
                 z_index: int = 0, visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)

        self.text = text
        self.font_size = font_size
        self.color = color or QColor(255, 255, 255)  # Default white text
        self.font = QFont()
        self.font.setPointSize(self.font_size)

    def get_bounding_box(self) -> QRectF:
        """Get the bounding box of the text."""
        # This is a simplified bounding box - for more precision, we'd use QFontMetrics
        return QRectF(self.x, self.y, 100, 20)  # Approximate size

    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the text contains the given scene point.
        For simplicity, we'll use a bounding box approximation.
        
        Args:
            point: Point in scene coordinates to check
        
        Returns:
            True if the text contains the point, False otherwise
        """
        # This is a simple approximation - for more precision, we'd need to
        # calculate the actual text bounds using QFontMetrics
        # For now, we'll use a 100x20 bounding box around the position
        return (self.x <= point.x() <= self.x + 100 and
                self.y <= point.y() <= self.y + 20)

    def paint(self, painter: QPainter):
        """
        Paint the text using the provided painter.
        
        Args:
            painter: QPainter to use for drawing the text
        """
        if not self.visible:
            return

        # Save the painter state
        painter.save()

        # Set font and color
        painter.setFont(self.font)
        painter.setPen(self.color)

        # Draw the text
        painter.drawText(QPointF(self.x, self.y + self.font_size), self.text)

        # Restore the painter state
        painter.restore()


class WidgetWrapper(Drawable):
    """
    A wrapper for embedding a QWidget in the scene.
    """
    
    def __init__(self, widget, x: float = 0, y: float = 0, z_index: int = 0, 
                 visible: bool = True, locked: bool = False):
        super().__init__(x, y, z_index, visible, locked)
        
        self.widget = widget
        self.width = widget.width() if hasattr(widget, 'width') else 100
        self.height = widget.height() if hasattr(widget, 'height') else 100

    def get_bounding_box(self) -> QRectF:
        """Get the bounding box of the widget wrapper."""
        return QRectF(self.x, self.y, self.width, self.height)

    def contains_point(self, point: QPointF) -> bool:
        """
        Check if the widget wrapper contains the given scene point.
        
        Args:
            point: Point in scene coordinates to check
        
        Returns:
            True if the widget wrapper contains the point, False otherwise
        """
        return (self.x <= point.x() <= self.x + self.width and
                self.y <= point.y() <= self.y + self.height)

    def paint(self, painter: QPainter):
        """
        Paint the widget wrapper using the provided painter.
        Note: Actual widget rendering is handled by Qt's widget system,
        so this is just a placeholder rectangle.
        
        Args:
            painter: QPainter to use for drawing the widget wrapper
        """
        if not self.visible:
            return

        # Save the painter state
        painter.save()

        # Draw a placeholder rectangle for the widget
        pen = QPen(QColor(100, 100, 100), 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(50, 50, 50, 100)))

        # Draw the rectangle
        rect = QRectF(self.x, self.y, self.width, self.height)
        painter.drawRect(rect)

        # Restore the painter state
        painter.restore()
