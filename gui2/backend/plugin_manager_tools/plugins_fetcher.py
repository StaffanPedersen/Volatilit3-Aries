import os


@staticmethod
def get_all_plugins(filepath=None, os_name=None):
    """Fetch all available plugins for the specified OS or all if OS is not specified."""
    try:
        start_path = os.path.dirname(os.path.realpath(__file__))
        volatility_file = find_volatility_file(start_path) if filepath is None else filepath

        if volatility_file is None:
            print("Volatility file not found.")
            return []

        base_dir = os.path.dirname(volatility_file)

        plugin_directories = {
            'Windows': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'windows'),
            'Linux': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'linux'),
            'Mac': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'mac')
        }
        plugin_list = []

        if os_name is None:
            print("OS is undefined.")
            for os_name, dir_path in plugin_directories.items():
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    plugins = [f"{os_name.lower()}.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if
                               os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                    plugin_list.append((os_name, plugins))
                else:
                    print(f"Directory {dir_path} does not exist or is not a directory.")
        else:
            print("OS is defined. {os_name}")
            dir_path = plugin_directories.get(os_name)
            if dir_path is not None and os.path.exists(dir_path) and os.path.isdir(dir_path):
                print(f"Directory {dir_path} exists and is a directory.")
                plugins = [f"{os_name.lower()}.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if
                           os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                plugin_list.append((os_name, plugins))
            else:
                print(f"Directory {dir_path} does not exist or is not a directory.")

        return plugin_list
    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []