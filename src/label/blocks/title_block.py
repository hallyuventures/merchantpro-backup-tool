from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout
import re

class TitleBlock(BaseBlock):

    def __init__(self, product, context):
        super().__init__(product)

        self.weight = product.weight.strip()
        self.name = self._remove_weight_from_name(
            product.name,
            self.weight,
        )

        self.font_size = (
            context.style.title_font_size
        )

    def _load_font(self):
        try:
            return ImageFont.truetype(
                "arialbd.ttf",
                self.font_size,
            )
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _remove_weight_from_name(
        name: str,
        weight: str,
    ) -> str:
        name = name.strip()

        if not weight:
            return name

        pattern = re.compile(
            rf"[\s,;-]*{re.escape(weight)}\s*$",
            re.IGNORECASE,
        )

        cleaned_name = pattern.sub("", name)

        return cleaned_name.rstrip(" ,;-")






    @staticmethod
    def _text_width(
        draw,
        text,
        font,
    ) -> int:
        left, top, right, bottom = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        return right - left

    @staticmethod
    def _text_height(
        draw,
        font,
    ) -> int:
        left, top, right, bottom = draw.textbbox(
            (0, 0),
            "Ag",
            font=font,
        )

        return bottom - top

    def _wrap_text(
        self,
        draw,
        text,
        font,
        max_width,
    ) -> list[str]:
        words = text.split()

        if not words:
            return []

        lines = []
        current_line = words[0]

        for word in words[1:]:
            candidate = f"{current_line} {word}"

            if (
                self._text_width(
                    draw,
                    candidate,
                    font,
                )
                <= max_width
            ):
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        return lines

    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        font = self._load_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        gap_px = context.mm_to_px(1.0)

        available_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        weight_width = 0

        if self.weight.strip():
            weight_width = self._text_width(
                draw,
                self.weight,
                font,
            )

        name_width = available_width

        if weight_width > 0:
            name_width = (
                available_width
                - weight_width
                - gap_px
            )

        lines = self._wrap_text(
            draw=draw,
            text=self.name,
            font=font,
            max_width=name_width,
        )

        text_height = self._text_height(
            draw,
            font,
        )

        line_spacing_px = context.mm_to_px(
            context.style.line_spacing_mm
        )

        line_height = (
            text_height
            + line_spacing_px
        )

        if lines:
            height = (
                len(lines) * text_height
                + (len(lines) - 1)
                * line_spacing_px
            )
        else:
            height = 0

        return BlockLayout(
            width=available_width,
            height=height,
            data={
                "font": font,
                "lines": lines,
                "line_height": line_height,
                "weight_width": weight_width,
                "gap_px": gap_px,
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
        lines = layout.data["lines"]
        line_height = layout.data["line_height"]
        weight_width = layout.data[
            "weight_width"
        ]

        current_y = y

        for line in lines:
            draw.text(
                (x, current_y),
                line,
                font=font,
                fill="black",
            )

            current_y += line_height

        if self.weight.strip():
            weight_x = (
                x
                + layout.width
                - weight_width
            )

            draw.text(
                (weight_x, y),
                self.weight,
                font=font,
                fill="black",
            )