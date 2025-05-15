#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from termcolor import colored

# ========== CONFIGURATION ========== #
# Get base directory and set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
LOG_DIR = os.path.join(BASE_DIR, "results")

BANNER = r"""
   ▄▄▄▄                                     ▄▄▄▄
 ▄█▀▀▀▀█                                   ██▀▀▀
 ██▄        ▄█████▄   ▄█████▄   ██▄████  ███████    ▄█████▄   ▄█████▄   ▄████▄
  ▀████▄   ██▀    ▀   ▀ ▄▄▄██   ██▀        ██       ▀ ▄▄▄██  ██▀    ▀  ██▄▄▄▄██
      ▀██  ██        ▄██▀▀▀██   ██         ██      ▄██▀▀▀██  ██        ██▀▀▀▀▀▀
 █▄▄▄▄▄█▀  ▀██▄▄▄▄█  ██▄▄▄███   ██         ██      ██▄▄▄███  ▀██▄▄▄▄█  ▀██▄▄▄▄█
  ▀▀▀▀▀      ▀▀▀▀▀    ▀▀▀▀ ▀▀   ▀▀         ▀▀       ▀▀▀▀ ▀▀    ▀▀▀▀▀     ▀▀▀▀▀
"""

TOOL_VERSION = "v3.0"
AUTHOR = "Created By Zerosocialcode"

# ========== UTILITY FUNCTIONS ========== #
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color, attrs=None):
    print(colored(text, color, attrs=attrs))

# ========== USER INTERFACE ========== #
def show_banner():
    clear_screen()
    print_colored(BANNER, 'blue', attrs=['bold'])
    print_colored("Advanced Phishing Toolkit", 'yellow', attrs=["bold"])
    print_colored(f"{TOOL_VERSION} {AUTHOR}", 'green', attrs=["bold"])
    print()

def display_message(message, level="info"):
    levels = {
        "info": ("[INFO]", "green"),
        "warning": ("[WARNING]", "yellow"),
        "error": ("[ERROR]", "red"),
    }
    prefix, color = levels.get(level, ("[INFO]", "green"))
    print_colored(f"{prefix} {message}", color)

# ========== LOG VIEWER ========== #
def view_logs():
    if not os.path.exists(LOG_DIR):
        display_message(f"The directory '{LOG_DIR}' does not exist.", level="error")
        return

    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.txt') or f.endswith('.log')]

    if not log_files:
        display_message("No log files found in the directory.", level="error")
        return

    display_message("Available Log Files:", level="info")
    for i, log in enumerate(log_files, 1):
        print_colored(f"  [{i}] {log}", 'cyan')

    try:
        choice = int(input(colored("\nSelect a log file by number > ", 'light_cyan')))
        if 1 <= choice <= len(log_files):
            log_path = os.path.join(LOG_DIR, log_files[choice - 1])
            os.system(f"cat {log_path}")
        else:
            display_message("Invalid selection.", level="error")
    except ValueError:
        display_message("Invalid input.", level="error")
    except KeyboardInterrupt:
        pass

    input(colored("\nPress Enter to continue...", 'yellow'))

# ========== SILENT SCRIPT RUNNER ========== #
def run_script(script_name):
    """Run scripts from the scripts directory"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    
    if not os.path.isfile(script_path):
        display_message(f"Script {script_name} not found in {SCRIPTS_DIR}", level="error")
        return

    try:
        process = subprocess.Popen(
            ['python3', script_path],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        process.wait()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        display_message(f"Error running script: {str(e)}", level="error")

# ========== MAIN MENU ========== #
def main_menu():
    show_banner()
    menu_options = [
        "[1] Website Cloner",
        "[2] Credential Harvester",
        "[3] View Captured Logs",
        "[4] Exit"
    ]
    for option in menu_options:
        print_colored(option, 'green', attrs=['bold'])
        print()

    try:
        choice = input(colored("SCARFACE > ", 'red', attrs=['bold']))
        return choice.strip()
    except KeyboardInterrupt:
        sys.exit(0)

# ========== MAIN FUNCTION ========== #
def main():
    # Silent checks
    if sys.version_info[0] < 3:
        sys.exit(0)

    try:
        from termcolor import colored
    except ImportError:
        sys.exit(0)

    while True:
        choice = main_menu()

        if choice == '1':
            run_script('cloner.py')
        elif choice == '2':
            run_script('harvester.py')
        elif choice == '3':
            view_logs()
            clear_screen()
        elif choice == '4':
            sys.exit(0)
        else:
            clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
