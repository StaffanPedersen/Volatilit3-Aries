import os

class ScanScreenBackend:
    def __init__(self):
        self.memory_dump = ""  # Add an attribute to store the selected file path

    def create_transparent_button(self, icon_filename):
        """Create path for the button icon."""
        # Determine the project root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
        print(f"Project root directory: {project_root}")

        # Construct the full path to the image
        icon_path = os.path.join(project_root, 'gui', 'frontend', 'images', icon_filename)
        print(f"Constructed icon path: {icon_path}")

        if not os.path.exists(icon_path):
            print(f"Image path does not exist: {icon_path}")
        else:
            print(f"Image path exists: {icon_path}")

        return icon_path

    def set_memory_dump(self, file_path):
        """Set the memory dump file path."""
        self.memory_dump = file_path
