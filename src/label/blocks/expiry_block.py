from .text_block import TextBlock


class ExpiryBlock(TextBlock):

    def __init__(self, product, context):
        super().__init__(
            product=product,
            text=f"Data Exp.: {product.expiry}",
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )