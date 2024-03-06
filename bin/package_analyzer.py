#!/usr/bin/python3

import logging
import sys

from package_analyzer.cli import parse_arguments
from package_analyzer.config_loader import load_config
from package_analyzer.package_analyzer import PackageAnalyzer


def main() -> None:
    args = parse_arguments()

    if args.quiet:
        logging.setLevel(logging.WARNING)

    package_analyzer = PackageAnalyzer(args.architecture, config["download"]["mirror_url"])
    package_analyzer.download_contents_file()
    package_analyzer.parse_contents_file()
    package_analyzer.print_top_packages(top_n=config["parse"]["top_n"])


if __name__ == "__main__":
    config = load_config()

    logging.basicConfig(level=getattr(logging, config["logging"]["level"]), format=config["logging"]["format"])

    try:
        main()
    except Exception as e:
        logging.error("Failed to execute the program", exc_info=True)
        sys.exit(1)
