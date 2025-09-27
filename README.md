<h1 align="center">
    <img src="resources/img/template.png" alt="Qt Ingot" width="128">
    <div align="center">Qt Ingot</div>
</h1>

Accelerate your desktop application development with Qt Ingot, a lightweight, themeable boilerplate for creating tab-based PyQt applications. Qt Ingot is designed to eliminate repetitive setup code, allowing you to focus on your application's core features from day one.

It provides a self-configuring main window, an intelligent SASS-based theming engine with automatic scaffolding, a data-driven menu bar, a flexible layout system, and a ready-to-use workspace, all powered by the `rune-lib` for zero-configuration asset management.

## Core Philosophy

The goal of `qt-ingot` is to provide a **"zero-effort" application frame**. The main application window should be smart enough to configure itself by discovering project-specific assets (like icons and themes) and providing safe, attractive defaults if they are missing.

## Features

*   **Declarative Configuration:** Configure your application with a simple Python dictionary. Set the title, icon, version, and more without writing boilerplate code.
*   **Data-Driven Menu Bar:** Define your entire menu structure in a dictionary. `qt-ingot` builds the `QMenuBar` for you, connecting actions to functions automatically.
*   **Flexible Layout System:** Easily add side panels to your application. The grid-based layout system allows for more complex UIs than simple tabbed views.
*   **Intelligent Theming Engine:**
    *   Powered by SASS for modern, maintainable stylesheets.
    *   **Automatic Scaffolding:** If no theme is found, `qt-ingot` creates a default theme for you.
    *   **Dynamic Theme Switching:** Discovered themes are automatically added to the "View" menu for on-the-fly theme changes.
*   **Ready-to-Use Workspace:** A flexible, tab-based workspace that can host any custom `QWidget`.
*   **Seamless Asset Management:** Built on top of `rune-lib` for intuitive asset path handling.

## Quickstart

To use `qt-ingot` in your own project, follow these steps.

1.  **Install the library:**
    ```bash
    uv add qt-ingot
    ```

2.  **Write your application:**
    Create a `main.py` file. Define your application's configuration, menu, and view content, then pass them to `IngotApp`.

    ```python
    # your_project/main.py
    import sys
    from PyQt6.QtWidgets import QApplication, QLabel
    from ingot.app import IngotApp
    from ingot.views.base import BaseView

    # 1. Define your application's configuration
    APP_CONFIG = {
        "title": "My Awesome Ingot App",
        "icon": "img.my_icon"  # A rune-lib friendly path
    }

    # 2. Define your menu structure
    MENU_CONFIG = {
        "File": [
            {"name": "Exit", "shortcut": "Esc", "function": sys.exit}
        ],
        "Help": [
            {"name": "About", "function": lambda: print("About This App!")}
        ]
    }

    # 3. Define the content for your tabs
    class MyCustomView(BaseView):
        def __init__(self):
            super().__init__()
            self.layout().addWidget(QLabel("This is my application's content!"))

    # 4. Launch the app
    def main():
        app = QApplication(sys.argv)
        
        main_window = IngotApp(view_factory=MyCustomView, config=APP_CONFIG)
        main_window.set_menu(MENU_CONFIG)

        # Add a side panel
        side_panel = QLabel("Side Panel")
        main_window.set_side_panel(side_panel, position='left')

        main_window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()
    ```

## Example

Here is the `main_tester.py` example running with the default theme that `qt-ingot` automatically generated.

## License

This project is licensed under the [MIT License](./LICENSE).

It also depends on other libraries which have their own licenses:
*   [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) (GPLv3 License)

## Attributions

This project uses some icons from [flaticon.com](https://www.flaticon.com/). The individual attributions are in the [attributions.md](./resources/attirbutions.md) file.