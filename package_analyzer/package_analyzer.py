from collections import defaultdict
import gzip
import os
import tempfile
import urllib.parse
import urllib.request
import urllib.error

from tqdm import tqdm


class PackageAnalyzer:
    def __init__(self, architecture, mirror_url: str):
        self._architecture = architecture
        self._mirror_url = mirror_url.format(architecture=architecture)

        self._contents_file_path = ""
        self._package_statistics = defaultdict(int)

    def download_contents_file(self) -> None:
        contents_file_path = os.path.join(tempfile.gettempdir(), os.path.basename(self._mirror_url))

        with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"Downloading Contents file for {self._architecture}", disable=None) as progress_bar:
            def update_progress_bar(blocknum, blocksize, totalsize):
                if blocknum == 0:
                    progress_bar.total = totalsize
                progress_bar.update(blocksize)

            try:
                self._contents_file_path, _ = urllib.request.urlretrieve(self._mirror_url, contents_file_path, reporthook=update_progress_bar)

            except urllib.error.URLError as e:
                raise Exception("Failed to download Contents file") from e

    def parse_contents_file(self):
        with gzip.open(self._contents_file_path, 'rt') as file:
            for line in file:
                packages = line.split()[-1].split(',')
                for package in packages:
                    self._package_statistics[package] += 1

    def print_top_packages(self, top_n=10) -> None:
        sorted_packages = sorted(self._package_statistics.items(), key=lambda x: x[1], reverse=True)[:top_n]
        header = f"{'#':<6}| {'Package'.ljust(35)}| {'File Count'}"
        print(header)
        print("-" * (len(header)))
        for index, (package, file_count) in enumerate(sorted_packages, start=1):
            print(f"{str(index).ljust(6)}| {package.ljust(35)}| {file_count}")
