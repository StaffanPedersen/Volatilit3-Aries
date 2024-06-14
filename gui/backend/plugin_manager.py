import os
from .volatility_finder import find_volatility_file

 #  get all available plugins for the specified OS or all if OS is not specified
def get_all_plugins(filepath=None, os_name=None):
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
            'Mac': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'mac'),
            'Community': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'community')
        }
        plugin_list = []

        # get plugins for the Community folder first
        if os_name is None or os_name == 'Community':
            dir_path = plugin_directories.get('Community')
            if dir_path and os.path.exists(dir_path) and os.path.isdir(dir_path):
                plugins = [f"community.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if
                           os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                plugin_list.append(('Community', plugins))

        # get plugins for specified OS or all OSes excluding 'Community'
        for current_os_name, dir_path in plugin_directories.items():
            if current_os_name != 'Community' and (os_name is None or current_os_name == os_name):
                if dir_path and os.path.exists(dir_path) and os.path.isdir(dir_path):
                    plugins = [f"{current_os_name.lower()}.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if
                               os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                    plugin_list.append((current_os_name, plugins))

        return plugin_list

    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []


