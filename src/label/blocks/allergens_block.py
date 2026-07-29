from .text_block import TextBlock


class AllergensBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.allergens.strip():
            text = f"ALERGENI: {product.allergens}"

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=True,
            align="left",
        )