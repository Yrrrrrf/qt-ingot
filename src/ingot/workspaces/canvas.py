# src/ingot/workspaces/canvas.py
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ..workspace import WorkspaceManager # Import the base WorkspaceManager
from ..layouts import LayoutNode # Import for type hinting if needed

class CanvasWorkspace(WorkspaceManager):
    """
    A specialized workspace where each tab's content is
    automatically wrapped in a QScrollArea for panning and zooming.

    This workspace inherits the layout building capabilities from
    WorkspaceManager and wraps the resulting content widget in a
    scroll area before adding it to the tab.

    Configuration Options:
    - All options supported by WorkspaceManager (view_config) are valid here.
    - Additional options can be added in the future (e.g., default scroll behavior).
    """
    def __init__(self, view_config: dict, canvas_config: dict | None = None):
        """
        Initializes the CanvasWorkspace.

        Args:
            view_config (dict): The configuration dictionary passed to the base
                                WorkspaceManager, containing layout_template,
                                widget_factories, or view_factory.
            canvas_config (dict, optional): Configuration specific to the CanvasWorkspace.
                                            Defaults to None. Example keys could be:
                                            - 'default_scroll_behavior': 'AsNeeded' | 'AlwaysOff' | 'AlwaysOn'
                                            - 'default_resize_policy': 'AdjustToContents' | 'Fixed'
        """
        # Store canvas-specific config
        self._canvas_config = canvas_config or {}

        # Initialize the parent WorkspaceManager with the view_config
        # This handles the layout building logic internally
        super().__init__(view_config)

        # Apply default canvas-specific settings after parent initialization
        self._apply_canvas_defaults()

    def _apply_canvas_defaults(self):
        """
        Applies default settings specific to the canvas behavior,
        potentially based on _canvas_config.
        """
        # Example: Set a default scroll behavior policy
        default_scroll_policy = self._canvas_config.get('default_scroll_behavior', 'AsNeeded')
        policies_map = {
            'AsNeeded': Qt.ScrollBarPolicy.ScrollBarAsNeeded,
            'AlwaysOff': Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
            'AlwaysOn': Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        }
        policy = policies_map.get(default_scroll_policy, Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # Note: This applies globally to *new* scroll areas created by new_tab.
        # Existing tabs would need their scroll areas updated separately if needed.
        # For now, we just store the default policy.
        self._default_scroll_policy = policy

    def new_tab(self):
        """
        Overrides the base method to wrap the generated content
        in a QScrollArea.
        """
        # First, build the content widget using the parent's logic (layout builder or factory).
        # This ensures the layout system from Phase 2 works seamlessly.
        original_content_widget = super().new_tab() # This calls WorkspaceManager.new_tab()

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName("ingotCanvasScrollArea") # Consistent naming for theming
        scroll_area.setWidgetResizable(True) # Crucial: Allows content to resize within the scroll area

        # Apply default scroll bar policies if configured
        scroll_area.setHorizontalScrollBarPolicy(self._default_scroll_policy)
        scroll_area.setVerticalScrollBarPolicy(self._default_scroll_policy)

        # Wrap the original content in the scroll area
        scroll_area.setWidget(original_content_widget)

        # Replace the content of the *last added tab* (the one created by super().new_tab())
        # with our new scroll area.
        # We rely on the fact that super().new_tab() adds a tab and sets the current index.
        current_index = self.currentIndex()
        if current_index >= 0: # Safety check
            # Remove the original content widget from the tab
            # Note: removeTab also deletes the widget by default, which we don't want.
            # We need to temporarily reparent it or use takeWidget.
            # The current implementation of WorkspaceManager.new_tab() returns the widget,
            # and it's added to the tab. QTabWidget owns the widget.
            # A safer way is to insert the scroll area at the same index,
            # using the same tab text, and then setCurrentIndex again.
            old_tab_text = self.tabText(current_index)
            old_tab_icon = self.tabIcon(current_index) # Preserve icon if any

            # Insert the new scroll area widget at the current index
            self.insertTab(current_index, scroll_area, old_tab_text)
            if not old_tab_icon.isNull():
                self.setTabIcon(current_index, old_tab_icon)

            # Remove the *old* tab (which now points to the original content widget)
            # We must set the current index to a different tab first to avoid issues
            # if the current tab is being removed. Let's remove the *next* tab added by super().
            # Actually, super().new_tab() adds one tab, sets current index. We are at that index.
            # We inserted the scroll area at the SAME index, pushing the original tab forward.
            # So the original tab is now at index + 1.
            self.removeTab(current_index + 1) # Remove the original content tab

            # Ensure the scroll area tab is the current one
            self.setCurrentIndex(current_index)

            # Return the original content widget for potential further manipulation by the caller,
            # although it's now embedded within the scroll area.
            return original_content_widget
        else:
            # This should theoretically not happen if super().new_tab() works correctly
            raise RuntimeError("CanvasWorkspace: new_tab failed - no current index after parent call.")

    # Optional Enhancement: Add methods for common canvas operations
    # Example: Zoom functionality (requires content widget support)
    def zoom_in(self, factor: float = 1.2):
        """Attempts to zoom in the content of the current tab."""
        current_widget = self.currentWidget()
        if current_widget and hasattr(current_widget, 'scale'):
            # Assumes the content widget has a 'scale' method or property
            current_scale = current_widget.scale()
            current_widget.scale(current_scale * factor, current_scale * factor)

    def zoom_out(self, factor: float = 1.2):
        """Attempts to zoom out the content of the current tab."""
        current_widget = self.currentWidget()
        if current_widget and hasattr(current_widget, 'scale'):
            current_scale = current_widget.scale()
            new_scale = current_scale / factor
            # Ensure scale doesn't go below a minimum (e.g., 0.1)
            if new_scale >= 0.1:
                current_widget.scale(new_scale, new_scale)
            else:
                print("Zoom out limited to prevent excessive scaling down.")

    def reset_zoom(self):
        """Attempts to reset the zoom level of the content of the current tab."""
        current_widget = self.currentWidget()
        if current_widget and hasattr(current_widget, 'reset_scale'):
            current_widget.reset_scale()
        elif current_widget and hasattr(current_widget, 'scale'):
            # Assuming scale(factor_x, factor_y) and initial scale is 1.0
            current_widget.scale(1.0, 1.0)