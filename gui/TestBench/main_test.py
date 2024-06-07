import sys
from PyQt5.QtWidgets import QApplication
from main_window_test import MainWindow

def main():
    """Main entry point for the application."""
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()