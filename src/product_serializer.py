from pathlib import Path
from urllib.parse import urlparse
from html_utils import html_to_text
from html_rewriter import HtmlRewriter
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

        product_data = {}

        for column in product_row.index:

            value = product_row[column]

            if hasattr(value, "item"):
                value = value.item()

            if str(value) == "nan":
                value = ""
            if isinstance(value, str) and "<" in value and ">" in value:

                product_data[column] = html_to_text(value)

            else:

                product_data[column] = value

        output = product_folder / "product.json"

        description = str(
            product_row["Descriere produs"]
        )

        description = HtmlRewriter.rewrite(description)

        description_file = (
            product_folder /
            "description.html"
        )

        description_file.write_text(
            description,
            encoding="utf-8"
        )

        with open(output, "w", encoding="utf-8") as f:

            json.dump(
                product_data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(f"[JSON] {output}")