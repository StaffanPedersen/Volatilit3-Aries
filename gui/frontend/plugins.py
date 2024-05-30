import os

def find_volatility_file(start_path, max_attempts=5):
    current_path = start_path
    attempts = 0

    while attempts < max_attempts:
        if 'vol.py' in os.listdir(current_path):
            return os.path.join(current_path, 'vol.py')

        current_path = os.path.dirname(current_path)
        attempts += 1

    return None


start_path = os.path.dirname(os.path.realpath(__file__))
volatility_file = find_volatility_file(start_path)


def get_all_plugins():
    """Return a list of available plugins for different operating systems."""
    try:
        # Explicitly set the base directory to the correct path
        base_dir = os.path.dirname(volatility_file)

        plugin_directories = {
            'Windows': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'windows'),
            'Linux': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'linux'),
            'Mac': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'mac')
        }

        plugin_list = []

        for os_name, dir_path in plugin_directories.items():
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                plugins = [f"{os_name.lower()}.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if
                           os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                plugin_list.append((os_name, plugins))
            else:
                print(f"Directory {dir_path} does not exist or is not a directory.")

        return plugin_list
    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []
