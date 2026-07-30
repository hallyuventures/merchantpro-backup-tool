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
    def _text_metrics(
        draw,
        text,
        font,
    ) -> tuple[int, int, int]:
        if not text:
            return 0, 0, 0

        left, top, right, bottom = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        return (
            right - left,
            bottom - top,
            top,
        )

    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        if not self.country_text and not self.expiry_text:
            return BlockLayout(
                width=0,
                height=0,
                data={},
            )

        font = self._load_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        available_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        gap_px = context.mm_to_px(2.0)

        (
            country_width,
            country_height,
            country_top,
        ) = self._text_metrics(
            draw,
            self.country_text,
            font,
        )

        (
            expiry_width,
            expiry_height,
            expiry_top,
        ) = self._text_metrics(
            draw,
            self.expiry_text,
            font,
        )

        same_line = (
            bool(self.country_text)
            and bool(self.expiry_text)
            and (
                country_width
                + gap_px
                + expiry_width
                <= available_width
            )
        )

        line_height = max(
            country_height,
            expiry_height,
        )

        line_spacing_px = context.mm_to_px(
            context.style.line_spacing_mm
        )

        if same_line:
            height = line_height
        elif self.country_text and self.expiry_text:
            height = (
                country_height
                + line_spacing_px
                + expiry_height
            )
        else:
            height = line_height

        return BlockLayout(
            width=available_width,
            height=height,
            data={
                "font": font,
                "same_line": same_line,
                "country_width": country_width,
                "country_height": country_height,
                "country_top": country_top,
                "expiry_width": expiry_width,
                "expiry_height": expiry_height,
                "expiry_top": expiry_top,
                "line_spacing_px": line_spacing_px,
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
        if layout.height == 0:
            return

        font = layout.data["font"]
        same_line = layout.data["same_line"]

        if same_line:
            if self.country_text:
                draw.text(
                    (
                        x,
                        y - layout.data["country_top"],
                    ),
                    self.country_text,
                    font=font,
                    fill="black",
                )

            if self.expiry_text:
                expiry_x = (
                    x
                    + layout.width
                    - layout.data["expiry_width"]
                )

                draw.text(
                    (
                        expiry_x,
                        y - layout.data["expiry_top"],
                    ),
                    self.expiry_text,
                    font=font,
                    fill="black",
                )

            return

        current_y = y

        if self.country_text:
            draw.text(
                (
                    x,
                    current_y
                    - layout.data["country_top"],
                ),
                self.country_text,
                font=font,
                fill="black",
            )

            current_y += (
                layout.data["country_height"]
                + layout.data["line_spacing_px"]
            )

        if self.expiry_text:
            draw.text(
                (
                    x,
                    current_y
                    - layout.data["expiry_top"],
                ),
                self.expiry_text,
                font=font,
                fill="black",
            )