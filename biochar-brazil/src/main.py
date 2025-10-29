# biochar-brazil/src/main.py

import sys
from cli import main as cli_main
from config import load_config

def main():
    # Load configuration settings
    config = load_config()

    # Execute the command-line interface
    cli_main(config)

if __name__ == "__main__":
    main()