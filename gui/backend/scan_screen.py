import os

class ScanScreenBackend:
    def __init__(self):
        self.memory_dump = ""

    def create_transparent_button(self, icon_filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
        print(f"Project root directory: {project_root}")

        icon_path = os.path.join(project_root, 'gui', 'frontend', 'images', icon_filename)

        return icon_path


    def set_memory_dump(self, file_path):
        self.memory_dump = file_path
