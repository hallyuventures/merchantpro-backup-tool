from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from product import Product


class LabelPreview:

    WIDTH = 696
    HEIGHT = 300

    def create(
            self,
            product: Product
    ):

        image = Image.new(
            "RGB",
            (self.WIDTH, self.HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        draw.text(
            (20, 20),
            product.name,
            fill="black",
            font=font
        )

        draw.line(
            (20, 55,676, 55),
            fill="black",
            width=1
        )

        draw.text(
            (20, 60),
            f"{product.price:.2f} RON",
            fill="black",
            font=font
        )

        draw.rectangle(
            (20, 130, 676, 220),
            outline="black",
            width=2
        )

        draw.text(
            (270, 165),
            "BARCODE",
            fill="black",
            font=font
        )
        
        output = Path("preview.png")

        image.save(output)

        print(f"[PREVIEW] {output}")