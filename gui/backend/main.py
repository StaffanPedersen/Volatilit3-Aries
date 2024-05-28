import argparse
import platform

def get_os_info():
    os_type = platform.system()
    os_details = platform.version()
    os_release = platform.release()
    
    return os_type, os_release, os_details


def parse_command(command):
    parser = argparse.ArgumentParser(description="Run specific functions from the command line.")
    parser.add_argument('command', choices=['1', '2', '3',  '4', 'exit'], help='The function to run')
    
    # Use the parser to parse the command provided
    args = parser.parse_args(command.split())
    
    if args.command == '1':
        print("1")
    elif args.command == '2':
        print("2")
    elif args.command == '3':
        print("3")
    elif args.command == '4':
        os_type, os_release, os_details = get_os_info()
        print(f"Operativsystem: {os_type}")
        print(f"Versjon: {os_release}")
        print(f"Detaljer: {os_details}")
    elif args.command == 'e':
        return True  # Signal to exit the program
    return False






def main():
    exit_program = False
    while not exit_program:
        user_input = input("Enter command (1: For quick default scan \n 2: idk, \n 3: \n 4: you'r OS\n exit: e): ")
        try:
            exit_program = parse_command(user_input)
        except SystemExit:
            # argparse throws a SystemExit exception if the command is invalid (e.g., unrecognized command)
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()