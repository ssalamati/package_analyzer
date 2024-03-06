from typing import Dict


def print_packages(package_stats: Dict[str, int]) -> None:
    """
    This function outputs a list of packages and their associated file counts
    to the console, displaying the data in a tabular format with headers. Each
    row represents a package, showing its rank, name, and the number of files
    associated with it.

    :param package_stats: A dictionary containing package names as keys and
        file counts as values.
    """
    header = f"{'#':<6}| {'Package'.ljust(35)}| {'File Count'}"
    print(header)
    print("-" * (len(header)))

    for index, (package, file_count) in enumerate(package_stats, start=1):
        print(f"{str(index).ljust(6)}| {package.ljust(35)}| {file_count}")
