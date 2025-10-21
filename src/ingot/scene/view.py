"""
Unified SceneView class that combines camera/view/controller logic.

This is the central QWidget that handles all rendering and input for the camera-on-a-scene paradigm.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QPointF, Qt, QRect
from PyQt6.QtGui import QPainter, QCursor, QMouseEvent, QWheelEvent, QRadialGradient, QColor, QKeyEvent
from typing import List
from .drawable import Drawable
from .manager import SceneManager


class SceneView(QWidget):
    """
    The SceneView widget renders the scene from the camera's perspective.
    It handles input events for camera navigation and renders Drawable
    items with proper camera transformations applied.
    
    This class combines the previous camera/controller and camera/view functionality
    into a single cohesive unit.
    """
    
    # Signal emitted when camera status changes (position, zoom, etc.)
    status_updated = pyqtSignal(dict)
    
    def __init__(self, scene_manager: SceneManager = None):
        super().__init__()
        
        # Initialize camera state
        self._position = QPointF(0.0, 0.0)  # Camera position (center of viewport in scene coordinates)
        self._zoom = 1.0  # Zoom level (1.0 = 100%)
        self._min_zoom = 0.01  # Minimum zoom level
        self._max_zoom = 100.0  # Maximum zoom level
        
        # Panning state
        self._is_panning = False
        self._pan_start_pos = QPointF(0, 0)
        self._camera_start_pos = QPointF(0, 0)
        
        # Mouse tracking
        self._last_mouse_pos = QPointF(0, 0)
        self._scope_visible = True  # Whether to show the cursor scope (crosshair)
        
        # Initialize scene data
        self._scene_manager = scene_manager or SceneManager()
        
        # Set up the widget
        self.setMinimumSize(400, 300)  # Minimum size for usability
        self.setMouseTracking(True)  # Enable mouse tracking for scope
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enable keyboard input
        
        # Set cursor to crosshair
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        
        # Create the "emptiness" background gradient
        self._create_background_gradient()

    def _create_background_gradient(self):
        """Create the radial gradient for the "emptiness" background."""
        pass  # Gradient is created dynamically in paintEvent for flexibility

    def set_scene_manager(self, scene_manager: SceneManager):
        """
        Set the scene manager to be used by this SceneView.
        
        Args:
            scene_manager: SceneManager object containing Drawable items to render
        """
        self._scene_manager = scene_manager
        self.update()

    def get_scene_manager(self) -> SceneManager:
        """Get the current scene manager."""
        return self._scene_manager

    def get_camera_position(self) -> QPointF:
        """Get the current camera position."""
        return self._position

    def get_zoom_level(self) -> float:
        """Get the current zoom level."""
        return self._zoom

    def set_zoom_level(self, level: float):
        """Set the zoom level with bounds checking."""
        self._zoom = max(self._min_zoom, min(self._max_zoom, level))
        self.update()  # Trigger repaint
        self._emit_status()

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse press events for panning and interaction.
        
        Args:
            event: Mouse event containing position and button information
        """
        from PyQt6.QtWidgets import QApplication
        
        # Track space key state for space+drag panning
        from PyQt6.QtWidgets import QApplication
        modifiers = QApplication.keyboardModifiers()
        alt_modifier = modifiers & Qt.KeyboardModifier.AltModifier
        # Using a custom method to check if space is pressed (will be implemented separately)
        # For now, we'll just use middle mouse and Alt+Left
        left_button = event.button() == Qt.MouseButton.LeftButton
        middle_button = event.button() == Qt.MouseButton.MiddleButton

        if (middle_button or (left_button and alt_modifier)):
            # Start panning with middle mouse button or Alt+Left
            self._pan_start_pos = QPointF(event.position().x(), event.position().y())
            self._camera_start_pos = QPointF(self._position)
            self._is_panning = True
        else:
            # Handle other mouse interactions - check if any scene items were clicked
            scene_pos = self._screen_to_scene(QPointF(event.position().x(), event.position().y()))
            
            # Check if any scene items were clicked
            for item in reversed(self._scene_manager.get_items()):  # Check topmost items first
                if hasattr(item, 'contains_point') and item.visible and not item.locked:
                    if item.contains_point(scene_pos):
                        if hasattr(item, 'on_clicked'):
                            item.on_clicked(scene_pos)
                        break

        self._last_mouse_pos = QPointF(event.position().x(), event.position().y())
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Handle mouse movement for panning and scope tracking.
        
        Args:
            event: Mouse event containing position information
        """
        mouse_pos = QPointF(event.position().x(), event.position().y())
        self._last_mouse_pos = mouse_pos

        # Update camera if panning
        if self._is_panning:
            # Calculate the offset in screen coordinates
            screen_delta = QPointF(
                mouse_pos.x() - self._pan_start_pos.x(),
                mouse_pos.y() - self._pan_start_pos.y()
            )
            
            # Convert screen delta to scene delta (inversely proportional to zoom)
            scene_delta = QPointF(
                -screen_delta.x() / self._zoom,
                -screen_delta.y() / self._zoom
            )
            
            # Update camera position
            new_pos = QPointF(
                self._camera_start_pos.x() + scene_delta.x(),
                self._camera_start_pos.y() + scene_delta.y()
            )
            
            self._position = new_pos

        self.update()  # Trigger repaint
        self._emit_status()
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Handle mouse release to end panning.
        
        Args:
            event: Mouse event containing position and button information
        """
        if event.button() == Qt.MouseButton.MiddleButton or (event.button() == Qt.MouseButton.LeftButton and (self._is_panning and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier)):
            self._is_panning = False
            self._pan_start_pos = QPointF(0, 0)
            self._camera_start_pos = QPointF(0, 0)
        
        event.accept()

    def wheelEvent(self, event: QWheelEvent):
        """
        Handle mouse wheel events for zooming.
        
        Args:
            event: Wheel event containing scroll information
        """
        # Get the mouse position in screen coordinates
        mouse_pos = QPointF(event.position().x(), event.position().y())
        
        # Determine if zooming in or out
        if event.angleDelta().y() > 0:
            # Zoom in
            self._zoom_to_cursor(mouse_pos, 1.25)
        else:
            # Zoom out
            self._zoom_to_cursor(mouse_pos, 1.0/1.25)
        
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        """
        Handle keyboard events for camera navigation.
        
        Args:
            event: Key event containing key information
        """
        step_size = 20.0  # Distance to move when using arrow keys
        zoom_factor = 1.25  # Factor for zoom in/out with keyboard
        
        # Adjust step size based on zoom level (so movement feels consistent)
        if self._zoom < 1.0:
            step_size = 20.0 / self._zoom
        else:
            step_size = 20.0 * self._zoom
        
        if event.key() == Qt.Key.Key_Left:
            self._position.setX(self._position.x() - step_size)
        elif event.key() == Qt.Key.Key_Right:
            self._position.setX(self._position.x() + step_size)
        elif event.key() == Qt.Key.Key_Up:
            self._position.setY(self._position.y() - step_size)
        elif event.key() == Qt.Key.Key_Down:
            self._position.setY(self._position.y() + step_size)
        elif event.key() == Qt.Key.Key_Plus or event.key() == Qt.Key.Key_Equal:
            # Zoom in
            self._zoom_to_cursor(self._last_mouse_pos if self._last_mouse_pos != QPointF(0, 0) else QPointF(self.width()/2, self.height()/2), 1.25)
        elif event.key() == Qt.Key.Key_Minus:
            # Zoom out
            self._zoom_to_cursor(self._last_mouse_pos if self._last_mouse_pos != QPointF(0, 0) else QPointF(self.width()/2, self.height()/2), 1.0/1.25)
        elif event.key() == Qt.Key.Key_0:
            # Reset zoom
            self._reset_zoom()
        elif event.key() == Qt.Key.Key_Home:
            # Center the camera at (0, 0) in the scene
            self._center_on(QPointF(0, 0))
        elif event.key() == Qt.Key.Key_H:
            # Home key - center view
            self._center_on(QPointF(0, 0))
        
        self._emit_status()
        event.accept()
    
    def _zoom_to_cursor(self, cursor_pos: QPointF, zoom_factor: float):
        """
        Zoom while keeping the point under the cursor stationary.
        
        Args:
            cursor_pos: Position of the cursor in screen coordinates
            zoom_factor: Factor to multiply the current zoom by
        """
        # Store the current camera state
        old_zoom = self._zoom
        old_position = QPointF(self._position)
        
        # Calculate the scene position under the cursor before zooming
        scene_pos_before = self._screen_to_scene(cursor_pos)
        
        # Apply the zoom
        new_zoom = max(self._min_zoom, min(self._max_zoom, self._zoom * zoom_factor))
        self._zoom = new_zoom
        
        # Calculate where the scene position under the cursor should be after zooming
        # (it should remain under the cursor)
        scene_pos_after = self._screen_to_scene_with_zoom(cursor_pos, self._zoom)
        
        # Adjust the camera position to keep the scene point under the cursor
        delta_scene = QPointF(
            scene_pos_after.x() - scene_pos_before.x(),
            scene_pos_after.y() - scene_pos_before.y()
        )
        
        self._position = QPointF(
            old_position.x() - delta_scene.x(),
            old_position.y() - delta_scene.y()
        )
    
    def _screen_to_scene_with_zoom(self, screen_pos: QPointF, zoom_level: float) -> QPointF:
        """
        Convert screen coordinates to scene coordinates with a specific zoom level.
        
        Args:
            screen_pos: Position in screen coordinates
            zoom_level: Zoom level to use for conversion
        
        Returns:
            Position in scene coordinates
        """
        # Calculate widget center
        widget_center_x = self.width() / 2.0
        widget_center_y = self.height() / 2.0
        
        # Adjust screen position relative to widget center
        rel_x = screen_pos.x() - widget_center_x
        rel_y = screen_pos.y() - widget_center_y
        
        # Calculate scene position
        scene_x = self._position.x() + rel_x / zoom_level
        scene_y = self._position.y() + rel_y / zoom_level
        
        return QPointF(scene_x, scene_y)
    
    def _screen_to_scene(self, screen_pos: QPointF) -> QPointF:
        """
        Convert screen coordinates to scene coordinates.
        
        Args:
            screen_pos: Position in screen coordinates (relative to this widget)
        
        Returns:
            Position in scene coordinates
        """
        return self._screen_to_scene_with_zoom(screen_pos, self._zoom)
    
    def _scene_to_screen(self, scene_pos: QPointF) -> QPointF:
        """
        Convert scene coordinates to screen coordinates.
        
        Args:
            scene_pos: Position in scene coordinates
        
        Returns:
            Position in screen coordinates
        """
        # Calculate widget center
        widget_center_x = self.width() / 2.0
        widget_center_y = self.height() / 2.0
        
        # Calculate screen coordinates
        screen_x = (scene_pos.x() - self._position.x()) * self._zoom + widget_center_x
        screen_y = (scene_pos.y() - self._position.y()) * self._zoom + widget_center_y
        
        return QPointF(screen_x, screen_y)

    def _emit_status(self):
        """Emit camera status information."""
        # Gather all relevant status information
        scene_pos = self._screen_to_scene(self._last_mouse_pos)
        
        # Sample color at mouse position if possible
        color = QColor(100, 100, 100)  # Default gray if no item is under cursor
        
        # Check if any drawable item is under the cursor and get its color
        for item in reversed(self._scene_manager.get_items()):
            if hasattr(item, 'contains_point') and item.visible and not item.locked:
                if item.contains_point(scene_pos):
                    # If item has a color property, use it
                    if hasattr(item, 'color'):
                        color = item.color
                    break
        
        status_data = {
            "screen_pos": self._last_mouse_pos,
            "scene_pos": scene_pos,
            "color": color,
            "zoom": self._zoom,
        }
        
        # Emit the signal with the status data
        self.status_updated.emit(status_data)

    def _reset_zoom(self):
        """Reset zoom to 1.0."""
        # Use the center of the viewport as the focal point
        center_pos = QPointF(self.width() / 2.0, self.height() / 2.0)
        self._zoom_to_cursor(center_pos, 1.0 / self._zoom)  # Calculate factor to get back to 1.0

    def _center_on(self, scene_pos: QPointF):
        """Center the camera on a specific scene position."""
        self._position = QPointF(scene_pos.x(), scene_pos.y())

    def paintEvent(self, event):
        """
        Handle the paint event by drawing the scene from the camera's perspective:
        - Layer 0: The "emptiness" radial gradient background
        - Layer 1: Drawable items transformed by camera position and zoom
        - Layer 2: Origin lines (X,Y axes at (0,0))
        - Layer 3: Crosshair scope if visible
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Apply camera transformation
        self._apply_camera_transform(painter)

        # Layer 0: Draw the "emptiness" radial gradient background
        self._draw_background(painter)

        # Layer 1: Draw scene items
        for item in self._scene_manager.get_items():
            if hasattr(item, 'visible') and item.visible:
                # Save painter state before painting each item
                painter.save()
                item.paint(painter)
                painter.restore()

        # Layer 2: Draw the origin lines (X,Y axes at (0,0) of scene coordinate system)
        self._draw_origin_lines(painter)

        # Layer 3: Draw the crosshair scope if visible (in screen coordinates)
        if self._scope_visible:
            self._draw_scope(painter)

    def _apply_camera_transform(self, painter):
        """
        Apply the camera transformation to the painter.
        
        Args:
            painter: QPainter to apply transformation to
        """
        # Reset any previous transformations
        painter.resetTransform()

        # Apply zoom
        painter.scale(self._zoom, self._zoom)

        # Apply camera offset (inverse of camera position to simulate moving through scene)
        painter.translate(
            -self._position.x(),
            -self._position.y()
        )

    def _draw_background(self, painter):
        """Draw the radial gradient background representing emptiness."""
        # Create a radial gradient centered in the scene coordinate system
        # Since we're drawing in the scene coordinate system (after transformations),
        # the gradient is drawn at the (0,0) origin of the scene
        center_x = 0
        center_y = 0
        
        # Calculate a reasonable radius based on the widget size
        widget_width = self.width()
        widget_height = self.height()
        
        # Temporarily reset transform to calculate actual widget size
        original_transform = painter.transform()
        painter.resetTransform()
        
        radius = max(widget_width, widget_height) / 2.0 / self._zoom

        # Create gradient
        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0, QColor(30, 30, 30))  # Darker center
        gradient.setColorAt(1, QColor(15, 15, 15))  # Darker edge

        # Save painter state, reset transform for background, restore
        painter.save()
        painter.resetTransform()

        # Draw a large rectangle with the gradient
        painter.fillRect(
            int(self._position.x() - widget_width / (2.0 * self._zoom)),
            int(self._position.y() - widget_height / (2.0 * self._zoom)),
            int(widget_width / self._zoom),
            int(widget_height / self._zoom),
            gradient
        )

        painter.restore()
        # Restore the original transform
        painter.setTransform(original_transform)

    def _draw_origin_lines(self, painter):
        """Draw the (0,0) origin lines on the scene coordinate system."""
        # Draw (0,0) origin lines - vertical and horizontal lines at (0,0) in scene coordinates
        # These lines represent the true coordinate system origin
        painter.setPen(
            QColor(255, 100, 100, 150)
        )  # Semi-transparent red for Y-axis (vertical line)
        # Draw vertical line (Y-axis) through (0,0)
        # We draw from a large negative to large positive Y to make sure it's visible
        painter.drawLine(0, -10000, 0, 10000)

        painter.setPen(
            QColor(100, 255, 100, 150)
        )  # Semi-transparent green for X-axis (horizontal line)
        # Draw horizontal line (X-axis) through (0,0)
        # We draw from a large negative to large positive X to make sure it's visible
        painter.drawLine(-10000, 0, 10000, 0)

        # Draw a small dot at the origin (0,0) to clearly mark the point
        painter.setPen(QColor(255, 255, 255, 200))  # White dot for origin
        painter.drawPoint(0, 0)

    def _draw_scope(self, painter):
        """Draw the crosshair scope at the current mouse position."""
        # Draw a simple crosshair at the mouse position
        # We draw this in screen coordinates so it's always visible at the cursor
        
        # Temporarily reset transform to draw the scope in screen coordinates
        painter.save()
        painter.resetTransform()

        # Use the original screen coordinates for drawing the crosshair
        x = int(self._last_mouse_pos.x())
        y = int(self._last_mouse_pos.y())

        # Make the crosshair 1px wide regardless of zoom
        painter.setPen(QColor(255, 255, 255, 200))  # Semi-transparent white

        # Draw horizontal line
        painter.drawLine(0, y, self.width(), y)
        # Draw vertical line
        painter.drawLine(x, 0, x, self.height())

        painter.restore()

    def toggle_scope(self):
        """Toggle the visibility of the cursor scope (crosshair)."""
        self._scope_visible = not self._scope_visible
        self.update()  # Trigger repaint to show/hide scope

    def zoom_in(self):
        """Increase zoom level."""
        self._zoom_to_cursor(
            self._last_mouse_pos if self._last_mouse_pos != QPointF(0, 0) else QPointF(self.width()/2, self.height()/2),
            1.25
        )

    def zoom_out(self):
        """Decrease zoom level."""
        self._zoom_to_cursor(
            self._last_mouse_pos if self._last_mouse_pos != QPointF(0, 0) else QPointF(self.width()/2, self.height()/2),
            1.0/1.25
        )

    def reset_zoom(self):
        """Reset zoom level to 1.0."""
        self._reset_zoom()

    def center_on_position(self, x: float, y: float):
        """Center the camera on a specific position in scene coordinates."""
        self._center_on(QPointF(x, y))

    def pan_by(self, dx: float, dy: float):
        """Pan the camera by a relative amount."""
        self._position.setX(self._position.x() + dx)
        self._position.setY(self._position.y() + dy)
        self.update()
