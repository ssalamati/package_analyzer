import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and parse Debian Contents file to get package statistics.")
    parser.add_argument("architecture", help="The architecture (e.g., amd64, arm64, mips) to fetch the Contents file for.")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help="Show program's version number and exit.")
    parser.add_argument('-q', '--quiet', action='store_true', help="Enable quiet mode, suppressing outputs.")
    return parser.parse_args()
