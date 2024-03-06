from collections import defaultdict
import gzip
import logging
import os
import re
import tempfile
from typing import Dict, List
import urllib.parse
import urllib.request
import urllib.error

import tenacity
from tqdm import tqdm


class PackageAnalyzer:
    """
    This class is designed to analyze Debian package statistics. It downloads
    the compressed Contents file for a specified architecture from a Debian
    mirror, parses the file, and outputs statistics of the top N packages with
    the most files associated with them. It efficiently processes the file
    without loading the entire contents into memory, making it suitable for
    handling large files.
    """

    def __init__(
        self, arch: str, mirror_url: str, retry_count: int = 3, wait_seconds: int = 5
    ):
        """
        Initializes the PackageAnalyzer with the specified architecture, mirror
        URL, retry count, and wait time.

        :param arch: Architecture to analyze
        :param mirror_url: The URL of the mirror
        :param retry_count: The number of retry attempts for downloading data
        :param wait_seconds: The waiting time between retries
        """
        self._arch = arch
        self._mirror_url = mirror_url.format(arch=arch)
        self.retry_count = retry_count
        self.wait_seconds = wait_seconds

    def get_package_stats(
        self, top_n: int = 10, validate_lines: bool = False
    ) -> Dict[str, int]:
        """
        Retrieves package statistics by downloading and parsing the contents
        file, then summarizing the data.

        :param top_n: The number of top packages to return
        :param validate_lines: Whether to validate each line in the file
        :return: A dictionary of package names and their occurrences
        """
        retry = tenacity.retry(
            stop=tenacity.stop_after_attempt(self.retry_count),
            wait=tenacity.wait_fixed(self.wait_seconds),
        )

        contents_file_path = retry(PackageAnalyzer._download_contents_file)(self)
        stats = self._parse_contents_file(contents_file_path, top_n, validate_lines)

        self._cleanup_downloaded_file(contents_file_path)

        return stats

    def _download_contents_file(self) -> str:
        """
        Downloads the contents file from the mirror URL.

        :return: The path to the downloaded file
        """
        target_file = os.path.join(
            tempfile.gettempdir(), os.path.basename(self._mirror_url)
        )

        with tqdm(
            unit="B",
            unit_scale=True,
            miniters=1,
            desc=f"Downloading Contents file for {self._arch}",
            disable=None,
        ) as progress_bar:

            def update_progress_bar(blocknum, blocksize, totalsize):
                if blocknum == 0:
                    progress_bar.total = totalsize
                progress_bar.update(blocksize)

            try:
                contents_file_path, _ = urllib.request.urlretrieve(
                    self._mirror_url, target_file, reporthook=update_progress_bar
                )
                return contents_file_path

            except urllib.error.URLError as e:
                raise Exception("Failed to download Contents file") from e

    def _parse_contents_file(
        self, contents_file_path: str, top_n: int, validate_lines: bool
    ) -> Dict[str, int]:
        """
        Parses the contents file to count the occurrences of each package.

        :param contents_file_path: The path to the contents file
        :param top_n: The number of top entries to return
        :param validate_lines: Whether to validate each line in the file
        :return: A sorted dictionary of packages and their counts
        """
        package_stats = defaultdict(int)

        with gzip.open(contents_file_path, "rt") as file:

            for line in file:
                if validate_lines and not self._is_contents_line_valid(line):
                    logging.warning(f"Invalid format detected in line: {line.strip()}")
                    continue

                packages = self._get_package_names(line)

                for package in packages:
                    package_stats[package] += 1

        return sorted(package_stats.items(), key=lambda x: x[1], reverse=True)[:top_n]

    @staticmethod
    def _is_contents_line_valid(contents_line: str) -> bool:
        """
        Validates the format of a line in the contents file.

        :param contents_line: The line to validate
        :return: True if valid, False otherwise
        """
        pattern = re.compile(r"^[^/].*\s+.*")
        return bool(pattern.match(contents_line))

    @staticmethod
    def _get_package_names(contents_line: str) -> List[str]:
        """
        Extracts package names from a line in the contents file.

        :param contents_line: The line from which to extract package names
        :return: A list of package names
        """
        packages = contents_line.rsplit(None, 1)[-1].split(",")
        return [package.rsplit("/", 1)[-1] for package in packages]

    @staticmethod
    def _cleanup_downloaded_file(file_path: str) -> None:
        """
        Deletes the downloaded file.

        :param file_path: The path to the file to be deleted
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been successfully deleted.")
