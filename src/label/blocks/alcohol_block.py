from .text_block import TextBlock


class AlcoholBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.alcohol_content.strip():
            text = (
                "CONTINUT ALCOOL: "
                f"{product.alcohol_content}"
            )

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )