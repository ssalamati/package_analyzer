import argparse
from collections import defaultdict
import gzip
import logging
import os
import tempfile
import urllib.request

import yaml
from tqdm import tqdm



def main():
    # Load the configuration from the YAML file
    with open('config.yml', 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    
    # Use the configuration for logging
    logging.basicConfig(level=getattr(logging, cfg['logging']['level']), format=cfg['logging']['format'])

    args = parse_arguments()
    
    contents_file_path = download_contents_file(cfg['download']['mirror_url'], args.architecture)

    if contents_file_path:
        logging.info("Download completed: %s", contents_file_path)
        package_statistics = parse_contents_file(contents_file_path)
        print_top_packages(package_statistics)
        os.remove(contents_file_path)
        logging.info("Temporary file cleaned up: %s", contents_file_path)
    else:
        logging.error("Failed to download Contents file.")

    
def download_contents_file(mirror_url, architecture):
    formatted_url = mirror_url.format(architecture=architecture)

    destination_path = os.path.join(os.path.join(tempfile.gettempdir(), f"Contents-{architecture}.gz"))
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"Downloading Contents file for {architecture}", disable=None) as progress_bar:
        def update_progress_bar(blocknum, blocksize, totalsize):
            if blocknum == 0:
                progress_bar.total = totalsize
            progress_bar.update(blocksize)
        try:
            urllib.request.urlretrieve(formatted_url, destination_path, reporthook=update_progress_bar)
            return destination_path
        except Exception as e:
            logging.error("Failed to download Contents file: %s", e)
            return None


def parse_contents_file(contents_file_path):
    package_statistics = defaultdict(int)
    with gzip.open(contents_file_path, 'rt') as file:
        for line in file:
            packages = line.split()[-1].split(',')
            for package in packages:
                package_statistics[package] += 1

    return package_statistics


def print_top_packages(package_statistics, top_n=10):
    sorted_packages = sorted(package_statistics.items(), key=lambda x: x[1], reverse=True)[:top_n]
    header = f"{'#':<6}| {'Package'.ljust(35)}| {'File Count'}"
    print(header)
    print("-" * (len(header)))
    for index, (package, file_count) in enumerate(sorted_packages, start=1):
        print(f"{str(index).ljust(6)}| {package.ljust(35)}| {file_count}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download and parse Debian Contents file to get package statistics.")
    parser.add_argument("architecture", help="The architecture (e.g., amd64, arm64, mips) to fetch the Contents file for.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
