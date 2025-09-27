from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

class MenuBarManager:
    """
    Manages the creation of a QMenuBar from a dictionary.
    """
    def build_from_dict(self, menu_data: dict, menu_bar: QMenuBar | None = None) -> QMenuBar:
        """
        Parses a dictionary to construct or update a QMenuBar.

        Args:
            menu_data: A dictionary defining the menu structure.
            menu_bar: An existing QMenuBar to add menus to. If None, a new one is created.

        Returns:
            A fully constructed or updated QMenuBar.
        """
        if menu_bar is None:
            menu_bar = QMenuBar()
        
        for menu_name, menu_items in menu_data.items():
            menu = QMenu(menu_name, menu_bar)
            for item in menu_items:
                action = QAction(item["name"], menu)
                if "shortcut" in item:
                    action.setShortcut(item["shortcut"])
                if "function" in item:
                    action.triggered.connect(item["function"])
                menu.addAction(action)
            menu_bar.addMenu(menu)
        return menu_bar
