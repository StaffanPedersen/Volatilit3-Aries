class ProgressManagerBackend:
    def __init__(self):
        self.progress_value = 0
        self.progress_max = 100

    def set_progress(self, value):
        """Set the progress value."""
        self.progress_value = value
        if value >= self.progress_max:
            self.progress_value = self.progress_max
        return self.progress_value

    def reset_progress(self):
        """Reset the progress value."""
        self.progress_value = 0
        return self.progress_value

    def get_progress(self):
        """Get the current progress value."""
        return self.progress_value

    def is_complete(self):
        """Check if the progress is complete."""
        return self.progress_value >= self.progress_max
