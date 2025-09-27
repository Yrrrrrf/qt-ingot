from PyQt6.QtWidgets import QTabWidget, QPushButton
from PyQt6.QtCore import Qt
from typing import Callable
from .views.base import BaseView

class WorkspaceManager(QTabWidget):
    """A tabbed workspace that dynamically creates new views using a factory."""
    def __init__(self, view_factory: Callable[[], BaseView]):
        super().__init__()
        self._view_factory = view_factory
        
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # Add a "new tab" button to the corner
        add_button = QPushButton("+")
        add_button.clicked.connect(self.new_tab)
        self.setCornerWidget(add_button, Qt.Corner.TopRightCorner)

        # Start with one tab open
        self.new_tab()

    def new_tab(self):
        """Creates a new tab using the provided view factory."""
        new_view = self._view_factory()
        index = self.addTab(new_view, f"Tab {self.count() + 1}")
        self.setCurrentIndex(index)
        return new_view

    def close_tab(self, index: int):
        """Closes the tab at the given index."""
        if self.count() > 1:
            self.removeTab(index)
        else:
            # Maybe show a message or prevent closing the last tab
            print("Cannot close the last tab.")