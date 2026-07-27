from pathlib import Path
from urllib.parse import urlparse
from html_utils import html_to_text
from html_rewriter import HtmlRewriter
from dataclasses import asdict
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

    def save(
            self,
            product_folder,
            product
    ):
        self._save_json(
            product_folder,
            product
        )

        self._save_html(
            product_folder,
            product
        )

    def _save_json(
            self,
            product_folder,
            product
    ):
        data = asdict(product)

        data["Descriere produs"] = html_to_text(
            product.description_html
        )

        output = product_folder / "product.json"

        with open(output, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(f"[JSON] {output}")

    def _save_html(
            self,
            product_folder,
            product
    ):
    
        description = HtmlRewriter.rewrite(
            product.description_html
        )

        description_file = (
            product_folder /
            "description.html"
        )

        description_file.write_text(
            description,
            encoding="utf-8"
        )   