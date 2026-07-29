from .text_block import TextBlock


class UsageBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.usage.strip():
            text = f"MOD DE UTILIZARE: {product.usage}"

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )