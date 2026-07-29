from .text_block import TextBlock


class TitleBlock(TextBlock):

    def __init__(self, product, context):
        super().__init__(
            product=product,
            text=product.name,
            font_size=context.style.title_font_size,
            bold=True,
            align="left",
        )