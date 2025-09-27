### **The Plan: Building a Self-Sufficient Theming Engine**

**Goal:** Transform `qt-ingot` from an application that *requires* a theme to one that *provides* a default theme if one isn't found, and actively helps the developer get started.

---

### **Step 1: Package the Default Theme Files *Inside* `qt-ingot`**

Before `qt-ingot` can provide a default theme, it needs to have one. We must package the necessary `.scss` files as part of the library itself, so they are always available after installation.

*   **1.1. Create the Internal Resource Directory:**
    *   Inside your `src/qt_ingot/` directory, create a new folder structure: `src/qt_ingot/resources/default_theme/`. This path is internal to the library and separate from the user's project resources.

*   **1.2. Add the Default Theme Files:**
    *   Inside `src/qt_ingot/resources/default_theme/`, create two files:
        *   `theme.scss`: A basic but good-looking default style for the main window, workspace, tabs, etc. You can copy a simplified version from your `image-alchemy` project to start.
        *   `_colors.scss`: A default color palette that `theme.scss` can `@import`.

*   **1.3. Configure `pyproject.toml` to Include These Files:**
    *   This is a critical step. Your build system (Hatch) needs to be told to include these non-Python files in the final package.
    *   You will need to add a configuration to your `pyproject.toml` file to specify that `qt_ingot/resources/**` should be included. This ensures that when someone installs your library, the default theme files are installed along with it.

---

### **Step 2: Implement the Theme Scaffolding in `ThemeManager`**

This is the user-assistance feature. The `ThemeManager` will check the user's project for themes, and if it finds none, it will create a default set for them.

*   **2.1. Enhance `ThemeManager`'s Initialization (`__init__`):**
    *   When an instance of `ThemeManager` is created, it should immediately perform a "scaffolding check."

*   **2.2. The Scaffolding Logic:**
    1.  Use `rune-lib` to check for the existence of the user's theme directory. This will be a `try...except AttributeError` block:
        ```
        try:
            user_themes_path = assets.themes
            # If this succeeds, the directory exists. Check if it's empty.
        except AttributeError:
            # The 'themes' group was not found. We need to create it.
        ```
    2.  **If the `themes` directory does NOT exist:**
        *   Log a helpful message to the console: `INFO: User 'themes' directory not found. Creating a default setup...`
        *   Use `pathlib` to create the `resources/themes/` and `resources/colors/` directories in the user's project.
        *   Copy the packaged `theme.scss` and `_colors.scss` (from Step 1) into the user's newly created directories.
        *   Log a success message: `SUCCESS: A default theme and color palette have been created at 'resources/themes/'. You can customize them to style your application.`

---

### **Step 3: Implement the Runtime Fallback Logic**

This logic ensures the application *always* has a theme to apply, even if the user deletes their theme files or specifies an invalid one.

*   **3.1. Create a Central `apply_theme(theme_name)` Method:**
    *   This method in `ThemeManager` will be the single point of entry for applying a theme.

*   **3.2. The Fallback Logic within `apply_theme`:**
    1.  **Attempt to Load User Theme:** Use `rune-lib` to find the theme requested by `theme_name` in the user's project (e.g., `assets.themes.custom`).
    2.  **Handle Failure:** If `rune-lib` raises an `AssetNotFoundError` (because the specific theme file is missing) or an `AttributeError` (because the whole `themes` group is missing), it means the user's theme is unavailable.
    3.  **Execute Fallback:**
        *   Log a warning: `WARNING: Theme '{theme_name}' not found. Applying the built-in default theme.`
        *   Load the content of the packaged `theme.scss` from *within the `qt-ingot` library's resources*.
    4.  **Compile and Apply:** Whether it loaded the user's theme or the internal default, compile the SASS content to CSS and apply it to the main application window.

---

### **Step 4: Integrate into `IngotApp` for Full Automation**

Finally, we tie this all together inside the main application class.

*   **4.1. Instantiate `ThemeManager` in `IngotApp`:**
    *   In the `IngotApp.__init__` method, create an instance of your new `ThemeManager`.
    *   `self.theme_manager = ThemeManager(self)` (passing the app instance so the manager can apply the stylesheet).
    *   The moment this line runs, the scaffolding check (Step 2) will automatically execute.

*   **4.2. Apply the Default Theme on Startup:**
    *   Immediately after creating the manager, call its `apply_theme` method with a default name.
    *   `self.theme_manager.apply_theme('theme')`
    *   Thanks to the fallback logic from Step 3, this call is now 100% safe. It will try to load the user's `theme.scss`, and if it fails for any reason, it will seamlessly apply the built-in default.

*   **4.3. Clean Up `main_tester.py`:**
    *   You can now remove all the manual theme-loading logic from `main_tester.py`. The `try...except` block for the theme is no longer needed. The application will handle its own styling.

By the end of these steps, your `qt-ingot` application will be truly self-sufficient. It will launch, theme itself correctly, and even help the developer by creating starter files if they are missing.
