from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout


class CountryBlock(BaseBlock):

    def __init__(self, product, context):
        super().__init__(product)

        self.country_text = ""

        if product.country.strip():
            self.country_text = (
                f"Produs in: {product.country}"
            )

        self.expiry_text = ""

        if product.expiry.strip():
            self.expiry_text = (
                f"Data Exp.: {product.expiry}"
            )

        self.font_size = (
            context.style.body_font_size
        )

    def _load_font(self):
        try:
            return ImageFont.truetype(
                "arial.ttf",
                self.font_size,
            )
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _text_size(
        draw,
        text,
        font,
    ) -> tuple[int, int]:
        if not text:
            return 0, 0

        left, top, right, bottom = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        return right - left, bottom - top

    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        font = self._load_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        available_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        country_width, country_height = (
            self._text_size(
                draw,
                self.country_text,
                font,
            )
        )

        expiry_width, expiry_height = (
            self._text_size(
                draw,
                self.expiry_text,
                font,
            )
        )

        height = max(
            country_height,
            expiry_height,
        )

        return BlockLayout(
            width=available_width,
            height=height,
            data={
                "font": font,
                "country_width": country_width,
                "expiry_width": expiry_width,
            },
        )

    def render(
        self,
        draw,
        x: int,
        y: int,
        layout: BlockLayout,
        context,
    ) -> None:
        font = layout.data["font"]

        if self.country_text:
            left, top, right, bottom = draw.textbbox(
                (0, 0),
                self.country_text,
                font=font,
            )

            draw.text(
                (
                    x,
                    y - top,
                ),
                self.country_text,
                font=font,
                fill="black",
            )

        if self.expiry_text:
            expiry_width = layout.data[
                "expiry_width"
            ]

            expiry_x = (
                x
                + layout.width
                - expiry_width
            )

            left, top, right, bottom = draw.textbbox(
                (0, 0),
                self.expiry_text,
                font=font,
            )

            draw.text(
                (
                    expiry_x,
                    y - top,
                ),
                self.expiry_text,
                font=font,
                fill="black",
            )