from .text_block import TextBlock


class PreparationBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.preparation.strip():
            text = (
                f"MOD DE PREPARARE: "
                f"{product.preparation}"
            )

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )