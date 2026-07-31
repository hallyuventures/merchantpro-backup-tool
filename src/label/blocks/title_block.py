import re

from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout


class TitleBlock(BaseBlock):

    def __init__(self, product, context):
        super().__init__(product)

        self.weight = str(
            product.weight or ""
        ).strip()

        self.name = self._remove_weight_from_name(
            str(product.name or ""),
            self.weight,
        )

        self.title_font_size = (
            context.style.title_font_size
        )

        self.weight_font_size = max(
            context.style.body_font_size,
            self.title_font_size - 5,
        )

    def _load_title_font(self):
        try:
            return ImageFont.truetype(
                "arialbd.ttf",
                self.title_font_size,
            )
        except OSError:
            return ImageFont.load_default()

    def _load_weight_font(self):
        try:
            return ImageFont.truetype(
                "arialbd.ttf",
                self.weight_font_size,
            )
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _remove_weight_from_name(
        name: str,
        weight: str,
    ) -> str:
        name = name.strip()

        if not name:
            return ""

        if weight:
            exact_pattern = re.compile(
                rf"[\s,;-]*{re.escape(weight)}\s*$",
                re.IGNORECASE,
            )

            cleaned_name = exact_pattern.sub(
                "",
                name,
            )

            if cleaned_name != name:
                return cleaned_name.rstrip(
                    " ,;-"
                )

        quantity_pattern = re.compile(
            r"""
            [\s,;-]*
            \d+(?:[.,]\d+)?
            \s*
            (?:
                kg |
                g |
                mg |
                l |
                ml |
                cl |
                bucati |
                bucata |
                pieces |
                piece |
                pcs
            )
            \.?
            \s*$
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        cleaned_name = quantity_pattern.sub(
            "",
            name,
        )

        return cleaned_name.rstrip(
            " ,;-"
        )

    @staticmethod
    def _text_width(
        draw,
        text,
        font,
    ) -> int:
        if not text:
            return 0

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

        lines: list[str] = []
        current_line = words[0]

        for word in words[1:]:
            candidate = (
                f"{current_line} {word}"
            )

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
        title_font = self._load_title_font()
        weight_font = self._load_weight_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        gap_px = context.mm_to_px(1.0)

        available_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        weight_width = self._text_width(
            draw,
            self.weight,
            weight_font,
        )

        max_weight_width = int(
            available_width * 0.40
        )

        same_line = (
            bool(self.weight)
            and weight_width <= max_weight_width
        )

        if same_line:
            name_width = (
                available_width
                - weight_width
                - gap_px
            )
        else:
            name_width = available_width

        name_lines = self._wrap_text(
            draw=draw,
            text=self.name,
            font=title_font,
            max_width=name_width,
        )

        weight_lines: list[str] = []

        if self.weight and not same_line:
            weight_lines = self._wrap_text(
                draw=draw,
                text=self.weight,
                font=weight_font,
                max_width=available_width,
            )

        title_height = self._text_height(
            draw,
            title_font,
        )

        weight_height = self._text_height(
            draw,
            weight_font,
        )

        line_spacing_px = context.mm_to_px(
            context.style.line_spacing_mm
        )

        title_line_height = (
            title_height
            + line_spacing_px
        )

        weight_line_height = (
            weight_height
            + line_spacing_px
        )

        name_height = 0

        if name_lines:
            name_height = (
                len(name_lines) * title_height
                + (
                    len(name_lines) - 1
                )
                * line_spacing_px
            )

        weight_block_height = 0

        if weight_lines:
            weight_block_height = (
                len(weight_lines) * weight_height
                + (
                    len(weight_lines) - 1
                )
                * line_spacing_px
            )

        section_spacing = 0

        if name_lines and weight_lines:
            section_spacing = line_spacing_px

        if same_line:
            height = max(
                name_height,
                weight_height,
            )
        else:
            height = (
                name_height
                + section_spacing
                + weight_block_height
            )

        return BlockLayout(
            width=available_width,
            height=height,
            data={
                "title_font": title_font,
                "weight_font": weight_font,
                "name_lines": name_lines,
                "weight_lines": weight_lines,
                "title_line_height": (
                    title_line_height
                ),
                "weight_line_height": (
                    weight_line_height
                ),
                "weight_width": weight_width,
                "same_line": same_line,
                "name_height": name_height,
                "section_spacing": (
                    section_spacing
                ),
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
        title_font = layout.data[
            "title_font"
        ]

        weight_font = layout.data[
            "weight_font"
        ]

        name_lines = layout.data[
            "name_lines"
        ]

        weight_lines = layout.data[
            "weight_lines"
        ]

        title_line_height = layout.data[
            "title_line_height"
        ]

        weight_line_height = layout.data[
            "weight_line_height"
        ]

        weight_width = layout.data[
            "weight_width"
        ]

        same_line = layout.data[
            "same_line"
        ]

        current_y = y

        for line in name_lines:
            left, top, right, bottom = (
                draw.textbbox(
                    (0, 0),
                    line,
                    font=title_font,
                )
            )

            draw.text(
                (
                    x,
                    current_y - top,
                ),
                line,
                font=title_font,
                fill="black",
            )

            current_y += title_line_height

        if self.weight and same_line:
            weight_x = (
                x
                + layout.width
                - weight_width
            )

            left, top, right, bottom = (
                draw.textbbox(
                    (0, 0),
                    self.weight,
                    font=weight_font,
                )
            )

            draw.text(
                (
                    weight_x,
                    y - top,
                ),
                self.weight,
                font=weight_font,
                fill="black",
            )

            return

        if weight_lines:
            current_y = (
                y
                + layout.data["name_height"]
                + layout.data["section_spacing"]
            )

        for line in weight_lines:
            line_width = self._text_width(
                draw,
                line,
                weight_font,
            )

            weight_x = (
                x
                + layout.width
                - line_width
            )

            left, top, right, bottom = (
                draw.textbbox(
                    (0, 0),
                    line,
                    font=weight_font,
                )
            )

            draw.text(
                (
                    weight_x,
                    current_y - top,
                ),
                line,
                font=weight_font,
                fill="black",
            )

            current_y += weight_line_height