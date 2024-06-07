class OutputManagerBackend:
    def __init__(self):
        self.headers = []
        self.data = []

    def set_data(self, headers, data):
        """Set the headers and data for the output manager."""
        self.headers = headers
        self.data = data

    def get_data(self):
        """Get the headers and data from the output manager."""
        return self.headers, self.data

    @staticmethod
    def parse_output(output):
        """Parse the output string into headers and data."""
        lines = output.strip().split('\n')
        headers = lines[0].split()
        data = [line.split() for line in lines[1:]]
        return headers, data
