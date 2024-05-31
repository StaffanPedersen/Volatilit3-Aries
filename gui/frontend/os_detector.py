import subprocess
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

def detect_os(memory_dump):
    """Detect the OS of the memory dump by running specific Volatility plugins."""
    start_path = os.path.dirname(os.path.realpath(__file__))
    volatility_file = find_volatility_file(start_path)

    if not volatility_file:
        print("Volatility script (vol.py) not found.")
        return None

    base_dir = os.path.dirname(volatility_file)
    vol_path = os.path.join(base_dir, "vol.py")

    os_plugins = {
        'windows': 'windows.pslist',
        'linux': 'linux.pslist',
        'mac': 'mac.pslist'
    }

    for os_name, plugin in os_plugins.items():
        command = ['python', vol_path, '-f', memory_dump, '-r', 'json', plugin]
        print(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return os_name
            else:
                if 'Unable to validate the plugin requirements' in result.stderr:
                    continue
        except Exception as e:
            print(f"Error running Volatility command: {e}")

    return None
