from .text_block import TextBlock


class ExtraInfoBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.extra_info.strip():
            text = (
                f"INFORMATII SUPLIMENTARE: "
                f"{product.extra_info}"
            )

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )