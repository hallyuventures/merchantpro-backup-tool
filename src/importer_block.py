from .text_block import TextBlock


class ImporterBlock(TextBlock):

    def __init__(self, product, context):
        text = ""

        if product.importer_distributor.strip():
            text = (
                "IMPORTATOR/DISTRIBUITOR: "
                f"{product.importer_distributor}"
            )

        super().__init__(
            product=product,
            text=text,
            font_size=context.style.body_font_size,
            bold=False,
            align="left",
        )