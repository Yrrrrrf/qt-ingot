<h1 align="center">
    <img src="resources/img/template.png" alt="Qt Ingot" width="128">
    <div align="center">Qt Ingot</div>
</h1>

Accelerate your desktop application development with Qt Ingot, a lightweight, themeable boilerplate for creating tab-based PyQt applications. Qt Ingot is designed to eliminate repetitive setup code, allowing you to focus on your application's core features from day one.

It provides a self-configuring main window, an intelligent SASS-based theming engine with automatic scaffolding, and a flexible workspace manager, all powered by the `rune-lib` for zero-configuration asset management.

## Core Philosophy

The goal of `qt-ingot` is to provide a **"zero-effort" application frame**. The main application window should be smart enough to configure itself by discovering project-specific assets (like icons and themes) and providing safe, attractive defaults if they are missing.

## Features

*   **Self-Configuring Window:** Automatically sets the window title, icon, and theme based on your project's `resources` directory (future versions will use a `config.json`).
*   **Intelligent Theming Engine:**
    *   Powered by SASS for modern, maintainable stylesheets.
    *   **Automatic Scaffolding:** If no theme is found in your project, `qt-ingot` creates a default `theme.scss` and `_colors.scss` for you to customize.
    *   **Robust Fallback:** Always ensures your application has a theme by using a bundled default if the user's theme fails to load.
*   **Ready-to-Use Workspace:** A flexible, tab-based workspace that can host any custom `QWidget`.
*   **Seamless Asset Management:** Built on top of `rune-lib` for intuitive and OS-independent asset path handling.

## Quickstart

To use `qt-ingot` in your own project, follow these steps.

1.  **Install the library:**
    ```bash
    uv add qt-ingot
    ```

2.  **Write your application:**
    Create a `main.py` file. You only need to define your custom view's content and pass it to `IngotApp`.

    ```python
    # your_project/main.py
    import sys
    from PyQt6.QtWidgets import QApplication, QLabel
    from qt_ingot.app import IngotApp
    from qt_ingot.views.base import BaseView
    from rune import assets, AssetNotFoundError

    # 1. Define the content for your tabs
    class MyCustomView(BaseView):
        def __init__(self):
            super().__init__()
            self.layout().addWidget(QLabel("This is my application's content!"))

    # 2. Launch the app
    def main():
        app = QApplication(sys.argv)
        
        # IngotApp handles window setup and theming automatically
        main_window = IngotApp(view_factory=MyCustomView)
        main_window.setWindowTitle("My Awesome App")
        
        # Use rune-lib to set the icon
        try:
            main_window.set_window_icon_from_path(assets.img.my_icon)
        except AssetNotFoundError:
            print("INFO: 'my_icon.png' not found. Using default icon.")

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