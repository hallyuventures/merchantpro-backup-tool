from .text_block import TextBlock


class CountryBlock(TextBlock):

    def __init__(self, product, context):
        super().__init__(
            product=product,
            text=f"Produs in: {product.country}",
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )