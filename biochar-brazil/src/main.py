"""
Main entry point for the Biochar-Brazil tool.
Runs the full CLI-based analysis pipeline.
"""

import sys
import logging
from src.cli import main as cli_main
from src.config import Config


def main():
    """
    Entry point for running the Biochar-Brazil analysis pipeline.
    """
    try:
        # Initialize configuration
        config = Config("configs/config.yaml")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logging.info("Loaded configuration from %s", config.config_file)

        # Run the CLI interface (handles args and execution flow)
        cli_main()

    except Exception as e:
        logging.exception("Fatal error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
