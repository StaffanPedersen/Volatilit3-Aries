import os

# Specify the absolute path to the volatility plugins directory
plugins_dir = "C:/Skole/Volatilit3-Aries/volatility3/framework/plugins"

# Initialize an empty list to store the plugin names
plugin_names = []

# Use os.walk to iterate through all subdirectories of plugins_dir
for dirpath, dirnames, filenames in os.walk(plugins_dir):
    for file in filenames:
        # Check if the file is a Python file
        if file.endswith('.py'):
            # Remove the .py extension to get the plugin name
            plugin_name = file[:-3]
            plugin_names.append(plugin_name)

# Now plugin_names list contains the names of all plugins

# Print all plugin names
for plugin in plugin_names:
    print(plugin)