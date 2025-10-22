# `v0.0.{some}`: Advanced DX and Interactivity

**Goal:** Implement a VS Code-style sidebar system and add tools that make the framework easier for other developers to use.

  * **Step 1: Design the "Activity Bar" and View Container**

      * **What:** Implement a system where a thin vertical bar on the left (the "Activity Bar") contains icons that switch the content of the entire left-side panel.
      * **Technical Details:**
          * The main left side panel will now contain a `QStackedWidget`. This widget holds all the possible sidebar views (e.g., Explorer, Search, Debug).
          * The "Activity Bar" will be a new, very thin widget placed to the left of the `QStackedWidget`. It will contain `QPushButtons` with icons.
          * Clicking a button on the Activity Bar will call `self.stacked_widget.setCurrentIndex(...)` to show the corresponding view.

  * **Step 2: Create a Sidebar View Manager**

      * **What:** A system for developers to register their own custom sidebars.
      * **Technical Details:**
          * Create a new `SidebarManager` class.
          * It will have a method like `register_view(icon_path, name, widget_factory)`.
          * The manager will be responsible for creating the Activity Bar buttons and adding the instantiated widgets to the `QStackedWidget`.

  * **Step 3: Implement an Explicit Focus System**

      * **What:** A centralized manager to track which part of the application has focus.
      * **Technical Details:**
          * Create a `FocusManager` class.
          * In `IngotApp`, connect to the global focus signal: `QApplication.instance().focusChanged.connect(self.focus_manager.on_focus_changed)`.
          * The `on_focus_changed(old_widget, new_widget)` method can be used to track history, which can make the Back/Forward navigation (from Phase 1) much more robust, as it could also track focus changes between sidebars and the main workspace.

  * **Step 4: Auto-Generate a Settings/Shortcuts Page**

      * **What:** Create a new view that can be opened from 
      the menu, which automatically li
      sts all registered actions and their shortcuts.
      * **Technical Details:**
          * This is a pure DX win. The `ActionManager` already holds a dictionary of all actions (`self._actions`).
          * Create a new view (e.g., `SettingsView`).
          * Inside it, iterate through `current_app_instance.action_manager._actions.values()`.
          * For each `QAction`, get its `text()` and `shortcut().toString()`.
          * Display this information in a `QTableWidget` for a clean, organized view.
