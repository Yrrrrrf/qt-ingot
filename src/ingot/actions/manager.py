"""
Action manager module for qt-ingot.

This module manages actions for the application menu system.
"""
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject
from typing import Dict, Callable, Any


class ActionManager(QObject):
    """
    Manages QAction instances and builds menus from configuration dictionaries.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._actions: Dict[str, QAction] = {}
        
    def register_action(self, action_id: str, action: QAction):
        """Register an action with the given ID."""
        self._actions[action_id] = action
        
    def get_action(self, action_id: str) -> QAction:
        """Get an action by its ID."""
        return self._actions.get(action_id)
        
    def build_menu_for_toolbar(self, menu: QMenu, menu_data: dict):
        """Build a menu from a dictionary configuration."""
        for menu_title, items in menu_data.items():
            for item in items:
                if item.get("separator"):
                    menu.addSeparator()
                else:
                    action_id = item.get("id")
                    name = item.get("name", "")
                    shortcut = item.get("shortcut", "")
                    func = item.get("function")
                    
                    action = QAction(name, self.parent())
                    if shortcut:
                        action.setShortcut(shortcut)
                    if func and callable(func):
                        action.triggered.connect(lambda checked, f=func: f())
                    
                    if action_id:
                        self.register_action(action_id, action)
                    
                    menu.addAction(action)