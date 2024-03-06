#!/usr/bin/python3

import logging
import sys

from package_analyzer.cli import parse_arguments
from package_analyzer.config_loader import load_config
from package_analyzer.package_analyzer import PackageAnalyzer
from package_analyzer.utils import print_packages
 

def main() -> None:
    """
    The main function that orchestrates the execution flow of the package
    analyzer tool. It parses command-line arguments, sets up logging based on
    the user's preference, initializes the PackageAnalyzer with the provided
    arguments and loaded configuration, and finally prints the package
    statistics after analyzing the downloaded Contents file.
    """
    args = parse_arguments()

    if args.quiet:
        logging.setLevel(logging.WARNING)

    package_analyzer = PackageAnalyzer(args.architecture, config["download"]["mirror_url"], retry_count=config["download"]["retry_count"], wait_seconds=config["download"]["wait_seconds"])
    package_stats = package_analyzer.get_package_stats(top_n=config["parse"]["top_n"], validate_lines=config["parse"]["validate_lines"])

    print_packages(package_stats)


if __name__ == "__main__":
    """
    The entry point of the script which loads the configuration, sets up
    logging, and calls the main function. It also handles any exceptions that
    occur during the execution of the main function, logging them as errors.
    """
    config = load_config()

    logging.basicConfig(level=getattr(logging, config["logging"]["level"]), format=config["logging"]["format"])

    try:
        main()
    except Exception as e:
        logging.error("Failed to execute the program", exc_info=True)
        sys.exit(1)
