import sys
from pathlib import Path

from src.label.engine import LabelEngine
from src.product_json_loader import ProductJSONLoader


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Utilizare: "
            "py test_json_label.py <product.json>"
        )
        raise SystemExit(1)

    json_path = Path(sys.argv[1])

    product = ProductJSONLoader.load(json_path)

    output_path = Path(
        f"label_{product.id}.png"
    )

    LabelEngine().render(
        product,
        str(output_path),
    )

    print(f"Produs: {product.name}")
    print(f"SKU: {product.sku or '[gol]'}")
    print(f"Tara: {product.country}")
    print(f"Greutate: {product.weight}")
    print(f"Eticheta: {output_path.resolve()}")


if __name__ == "__main__":
    main()