from .text_block import TextBlock


class IngredientsBlock(TextBlock):

    def __init__(self, product, context):
        super().__init__(
            product=product,
            text=f"INGREDIENTE: {product.ingredients}",
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )