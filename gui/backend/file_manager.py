import subprocess

def get_memory_dump_metadata(dump_file_path):
    # Ensure the file path is provided and presumably valid (you might want to add more checks)
    if not dump_file_path:
        print("No dump file path provided.")
        return

    # Construct the command to retrieve basic metadata from the memory dump
    # This uses the 'imageinfo' plugin which is useful for gathering metadata about the memory image
    command = ['python', 'vol.py', '-f', dump_file_path, 'imageinfo']


    print("Running command:", ' '.join(command))
    try:
        # Execute the command using subprocess.run
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Output the command results
        print("Metadata extraction was successful:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        print("Error: Failed to extract metadata. The command returned a non-zero exit status.")
        print(f"Command output:\n{e.output}")
    except FileNotFoundError:
        print("Error: The 'vol.py' script was not found. Please ensure it is in the correct path.")
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {str(e)}")

# Example usage:
dump_file_path = '/path/to/memory.dmp'  # Replace this with the path to your dump file
get_memory_dump_metadata(dump_file_path)
