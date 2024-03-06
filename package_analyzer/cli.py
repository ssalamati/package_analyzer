import argparse

from package_analyzer import __version__


def parse_arguments() -> argparse.Namespace:
    """
    Parse and return the command-line arguments provided by the user.

    :return: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Download and parse Debian Contents file to get package statistics.")

    parser.add_argument("architecture", help="The architecture (e.g., amd64, arm64, mips) to fetch the Contents file for.")
    parser.add_argument('-v', '--version', action='version', version="%(prog)s " + __version__, help="Show program's version number and exit.")
    parser.add_argument('-q', '--quiet', action='store_true', help="Enable quiet mode, suppressing outputs.")

    return parser.parse_args()
