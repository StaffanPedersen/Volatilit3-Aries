class OutputManagerBackend:
    def __init__(self):
        self.headers = []
        self.data = []

    def set_data(self, headers, data):
        """Set the headers and data."""
        self.headers = headers
        self.data = data

    def get_data(self):
        """Get the headers and data."""
        return self.headers, self.data
