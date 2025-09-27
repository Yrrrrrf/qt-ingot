import sys
from PyQt6.QtWidgets import QApplication, QLabel

from rune import AssetNotFoundError, assets

from ingot.app import IngotApp
from ingot.views.base import BaseView


# --- Step 1: Define the application's custom view ---
# This remains the same. The developer provides the content for the tabs.
class MyTestView(BaseView):
    """A simple custom view that displays a label."""
    def __init__(self):
        super().__init__()
        label = QLabel("This is a custom view inside a new tab!\n\nClose this tab or press '+' to create another one.")
        label.setStyleSheet("font-size: 20px;")
        self.layout().addWidget(label)

# --- Step 2: The Main Application Logic ---
def main():
    app = QApplication(sys.argv)

    # --- Use `qt-ingot` to build the window ---
    # The IngotApp will now automatically handle theme scaffolding and loading on its own.
    # We no longer need to find and apply a theme manually.
    main_window = IngotApp(view_factory=MyTestView)
    main_window.setWindowTitle("My Qt Ingot Tester App")

    # --- Use `rune` to find other assets like icons ---
    # This part is still manual for now, which is perfectly fine.
    try:
        app_icon = assets.img.template
        main_window.set_window_icon_from_path(app_icon)
    except AssetNotFoundError as e:
        # If the icon isn't found, we just print a message.
        # The app will run with the system's default icon.
        print(f"INFO: Could not find app icon, using default. ({e})")

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
