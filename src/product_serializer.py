from pathlib import Path
from urllib.parse import urlparse
from html_utils import html_to_text
import json
import re


class ProductSerializer:

    def __init__(self, output_folder="backup"):

        self.output = Path(output_folder)
        self.output.mkdir(exist_ok=True)

    def sanitize_filename(self, name: str) -> str:

        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        name = re.sub(r"\s+", " ", name)

        return name.strip()

    def save(self, product_folder, product_row, images):

        data = {}

        for column in product_row.index:

            value = product_row[column]

            if hasattr(value, "item"):
                value = value.item()

            if str(value) == "nan":
                value = ""
            if isinstance(value, str) and "<" in value and ">" in value:

                data[column] = html_to_text(value)

            else:

                data[column] = value

        image_files = []

        for url in images:

            filename = Path(urlparse(url).path).name
            image_files.append(filename)

        data["Imagini locale"] = image_files

        output = product_folder / "product.json"

        with open(output, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(f"[JSON] {output}")