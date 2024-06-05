import os

def find_volatility_file(start_path, max_attempts=5):
    """Find the vol.py file used to run Volatility."""
    current_path = start_path
    attempts = 0

    while attempts < max_attempts:
        if 'vol.py' in os.listdir(current_path):
            return os.path.join(current_path, 'vol.py')

        current_path = os.path.dirname(current_path)
        attempts += 1

    return None