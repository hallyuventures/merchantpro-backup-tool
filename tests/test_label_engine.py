import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.label.engine import LabelEngine
from src.product import Product


def make_product(**changes) -> Product:
    data = {
        "id": 1,
        "name": "Produs test, 100g",
        "sku": "TEST-001",
        "brand": "Test",
        "category": "K-Food",
        "price": 0,
        "country": "Coreea de Sud",
        "weight": "100g",
        "alcohol_content": "",
        "ingredients": "Apa, faina, zahar si sare.",
        "allergens": "",
        "nutrition": "",
        "preparation": "",
        "usage": "",
        "expiry": "A se vedea pe ambalaj.",
        "extra_info": "",
        "supplier": "",
        "importer_distributor": "",
    }

    data.update(changes)

    return Product(**data)


class LabelEngineTest(unittest.TestCase):

    def setUp(self):
        self.engine = LabelEngine()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def render(self, product, filename="label.png") -> Image.Image:
        output = Path(self.temp_dir.name) / filename

        self.engine.render(
            product,
            output_path=str(output),
        )

        self.assertTrue(output.exists())

        with Image.open(output) as image:
            return image.copy()

    def test_label_uses_printable_width(self):
        image = self.render(make_product())

        self.assertEqual(
            image.width,
            self.engine.context.printable_width_px,
        )

        self.assertEqual(image.width, 697)

    def test_label_respects_minimum_length(self):
        product = make_product(
            ingredients="",
            expiry="",
            country="",
        )

        image = self.render(product)

        minimum_height = self.engine.context.mm_to_px(
            self.engine.printer.min_length_mm
        )

        self.assertGreaterEqual(
            image.height,
            minimum_height,
        )

    def test_long_content_increases_label_height(self):
        short_label = self.render(
            make_product(
                ingredients="Apa si sare.",
            ),
            "short.png",
        )

        long_label = self.render(
            make_product(
                ingredients=(
                    "Apa, faina de grau, zahar, ulei vegetal, "
                    "amidon, sare, sirop de glucoza, arome, "
                    "condimente si alte ingrediente. "
                ) * 5,
            ),
            "long.png",
        )

        self.assertGreater(
            long_label.height,
            short_label.height,
        )

    def test_empty_optional_blocks_do_not_change_height(self):
        base_product = make_product()

        empty_optional_product = make_product(
            allergens="",
            preparation="",
            usage="",
            extra_info="",
            alcohol_content="",
            importer_distributor="",
        )

        base_label = self.render(
            base_product,
            "base.png",
        )

        empty_label = self.render(
            empty_optional_product,
            "empty.png",
        )

        self.assertEqual(
            base_label.height,
            empty_label.height,
        )

    def test_optional_content_increases_height_when_needed(self):
        short_label = self.render(
            make_product(),
            "without_usage.png",
        )

        detailed_label = self.render(
            make_product(
                usage=(
                    "Aplicati produsul pe pielea curata si "
                    "masati pana la absorbtia completa. "
                ) * 4,
            ),
            "with_usage.png",
        )

        self.assertGreater(
            detailed_label.height,
            short_label.height,
        )


if __name__ == "__main__":
    unittest.main()