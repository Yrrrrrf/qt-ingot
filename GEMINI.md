# Plan: Evolving `qt-ingot` into a Zero-Effort Framework

This plan outlines the next development phases for `qt-ingot`. The goal is to build upon the solid v0.0.1 foundation to create a truly "zero-effort" application frame that is highly configurable, flexible, and powerful, drastically reducing boilerplate for the end user.

## Phase 1: Implement the Self-Configuring `IngotApp`

**Goal:** Make `IngotApp` capable of configuring itself from a Python dictionary, with an optional fallback to a `config.json` file. This eliminates the need for manual `setWindowTitle` and `setWindowIcon` calls in the user's script.

### 1.1: Enhance `IngotApp`'s Constructor
-   Modify the `IngotApp.__init__` method to accept an optional `config` dictionary.
-   This dictionary will be the primary source for application settings.
-   The new signature should be:
    ```python
    def __init__(self, view_factory: type[BaseView], config: dict | None = None):
    ```

### 1.2: Create the Configuration Logic
-   Inside `IngotApp`, create a new private method, `_load_configuration(self, config: dict | None)`.
-   This method will establish a clear priority for settings:
    1.  Use the `config` dictionary if it's provided.
    2.  If not, use `rune-lib` to *try* to find and load `resources/data/config.json`.
    3.  If neither is found, fall back to sensible defaults (e.g., "Qt Ingot Application", no icon).
-   Inside this method, set the window title, size, and icon based on the loaded configuration.

### 1.3: Update the Example
-   Modify `examples/main_tester.py` to showcase this new, cleaner workflow. The user will define a `APP_CONFIG` dictionary and pass it directly to `IngotApp`.

    ```python
    # main_tester.py (New Version)
    APP_CONFIG = {
        "title": "My Awesome Ingot App",
        "version": "1.0.0",
        "author": "My Name",
        "icon": "img.my_icon" # A rune-lib friendly path
    }
    
    main_window = IngotApp(view_factory=MyTestView, config=APP_CONFIG)
    ```

## Phase 2: Integrate a Data-Driven `MenuBar`

**Goal:** Re-introduce the powerful `MenuBar` from your original projects, allowing the developer to define the entire menu structure in a simple dictionary, completely abstracting away the PyQt6 implementation.

### 2.1: Create the `MenuBarManager`
-   Create a new module, e.g., `src/ingot/menu/manager.py`.
-   The `MenuBarManager` class will have one primary method, `build_from_dict(menu_data: dict) -> QMenuBar`.
-   This method will parse a dictionary (e.g., `{'File': [{'name': 'Exit', 'shortcut': 'Esc', 'function': app.quit}]}`) and construct the `QMenuBar` with all its `QMenu`s and `QAction`s.

### 2.2: Integrate into `IngotApp`
-   In `IngotApp.__init__`, instantiate your new `MenuBarManager`.
-   Add a public method `set_menu(self, menu_data: dict)`.
-   This method will use the `MenuBarManager` to build the menu bar and then call `self.setMenuBar()` to attach it to the main window.

### 2.3: Update the Example
-   In `examples/main_tester.py`, define a sample `MENU_CONFIG` dictionary.
-   After creating the `IngotApp` instance, call `main_window.set_menu(MENU_CONFIG)` to demonstrate how easily the menu can be added.

## Phase 3: Implement a Flexible Layout System

**Goal:** Restore the ability to have complex layouts (like a side panel) by introducing a `Display` container, making `qt-ingot` suitable for more than just simple tabbed views.

### 3.1: Create the `Display` Class
-   Create a new `src/ingot/display.py` module.
-   The `Display` class will inherit from `QFrame` and use a `QGridLayout`.
-   This `Display` will become the central widget of `IngotApp`. It will contain the `WorkspaceManager` by default in a specific grid cell (e.g., `(0, 1)`).

### 3.2: Expose Layout Management Methods
-   `IngotApp` should now proxy layout control to the `Display` widget.
-   Add a user-friendly method like `set_side_panel(self, widget: QWidget, position: str = 'left')`.
-   This method will add the provided widget to the `Display`'s grid layout at the correct position (e.g., `(0, 0)` for 'left').

### 3.3: (Optional) Update the Example
-   Briefly modify `main_tester.py` to add a simple `QLabel` as a side panel to prove the concept and demonstrate the new API.

## Phase 4: Final Polish and Documentation

**Goal:** Refine the existing features and update the documentation to reflect the library's new capabilities, ensuring it's easy for others (and your future self) to use.

### 4.1: Enhance the `ThemeManager`
-   With the `MenuBar` in place, you can now add a "Change Theme" feature.
-   The `ThemeManager` can be updated to use `rune-lib` to discover all `.scss` files within the user's theme directory.
-   These discovered themes can be dynamically added as actions to the "View" menu, allowing for on-the-fly theme switching.

### 4.2: Update the `README.md`
-   Thoroughly update the Quickstart and Features sections to reflect the new configuration system (`config` dictionary), the `MenuBarManager`, and the layout system.
-   Provide clear examples for all major features.

### 4.3: Add Docstrings
-   Ensure all new classes and public methods created in Phases 1-3 have clear, concise docstrings explaining their purpose, arguments, and return values.

By following this plan, you will transform `qt-ingot` from a solid foundation into an exceptionally powerful and developer-friendly framework.
