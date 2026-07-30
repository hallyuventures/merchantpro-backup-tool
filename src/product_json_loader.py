import html
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from src.product import Product


class _HTMLTextExtractor(HTMLParser):
    """
    Extrage textul din HTML fără să introducă spații în mijlocul
    cuvintelor întrerupte de taguri inline.
    """

    BLOCK_TAGS = {
        "div",
        "p",
        "br",
        "li",
        "tr",
        "td",
        "section",
        "article",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() == "br":
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCK_TAGS:
            self.parts.append(" ")

    def get_text(self) -> str:
        return "".join(self.parts)


def clean_text(value: Any) -> str:
    """
    Transformă HTML-ul MerchantPro în text simplu și convertește
    valorile lipsă în șir gol.
    """

    if value is None:
        return ""

    if isinstance(value, float) and math.isnan(value):
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "none", "null"}:
        return ""

    parser = _HTMLTextExtractor()
    parser.feed(text)
    parser.close()

    cleaned = parser.get_text()
    cleaned = html.unescape(cleaned)
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()


class ProductJSONLoader:

    @staticmethod
    def load(path: str | Path) -> Product:
        json_path = Path(path)

        if not json_path.exists():
            raise FileNotFoundError(
                f"Fisierul nu exista: {json_path}"
            )

        try:
            with json_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"JSON invalid: {json_path}"
            ) from error

        return Product(
            id=int(data.get("id", 0)),
            name=clean_text(data.get("name")),
            sku=clean_text(data.get("sku")),
            brand=clean_text(data.get("brand")),
            category=clean_text(data.get("category")),
            price=float(data.get("price") or 0),
            country=clean_text(data.get("country")),
            weight=clean_text(data.get("weight")),
            alcohol_content=clean_text(
                data.get("alcohol_content")
            ),
            ingredients=clean_text(
                data.get("ingredients")
            ),
            allergens=clean_text(
                data.get("allergens")
            ),
            nutrition=clean_text(
                data.get("nutrition")
            ),
            preparation=clean_text(
                data.get("preparation")
            ),
            usage=clean_text(
                data.get("usage")
            ),
            expiry=clean_text(
                data.get("expiry")
            ),
            extra_info=clean_text(
                data.get("extra_info")
            ),
            importer_distributor=clean_text(
                data.get("importer_distributor")
            ),
        )