from pathlib import Path
from urllib.parse import urlparse

import requests


class Downloader:

    def __init__(self, output_folder="backup"):

        self.output = Path(output_folder)
        self.output.mkdir(exist_ok=True)

    def download(self, product_id: int, url: str):

        product_folder = self.output / str(product_id)
        product_folder.mkdir(exist_ok=True)

        filename = Path(urlparse(url).path).name

        destination = product_folder / filename

        if destination.exists():
            print(f"[SKIP] {filename}")
            return

        print(f"[GET ] {filename}")

        response = requests.get(url, timeout=30)

        response.raise_for_status()

        destination.write_bytes(response.content)

        print(f"[ OK ] {destination}")