from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout


class ImporterBlock(BaseBlock):

    def __init__(self, product, context):
        super().__init__(product)

        raw_text = str(
            product.importer_distributor or ""
        ).strip()

        self.sections = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

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
        if not self.sections:
            return BlockLayout(
                width=0,
                height=0,
                data={},
            )

        font = self._load_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        max_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        wrapped_sections = [
            self._wrap_text(
                draw=draw,
                text=section,
                font=font,
                max_width=max_width,
            )
            for section in self.sections
        ]

        left, top, right, bottom = draw.textbbox(
            (0, 0),
            "Ag",
            font=font,
        )

        text_height = bottom - top

        line_spacing = context.mm_to_px(
            context.style.line_spacing_mm
        )

        section_spacing = context.mm_to_px(
            context.style.section_spacing_mm
        )

        line_height = text_height + line_spacing

        total_lines = sum(
            len(lines)
            for lines in wrapped_sections
        )

        height = 0

        if total_lines:
            height = (
                total_lines * text_height
                + (total_lines - len(wrapped_sections))
                * line_spacing
                + (len(wrapped_sections) - 1)
                * section_spacing
            )

        return BlockLayout(
            width=max_width,
            height=height,
            data={
                "font": font,
                "wrapped_sections": wrapped_sections,
                "line_height": line_height,
                "section_spacing": section_spacing,
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
        wrapped_sections = layout.data[
            "wrapped_sections"
        ]
        line_height = layout.data[
            "line_height"
        ]
        section_spacing = layout.data[
            "section_spacing"
        ]

        current_y = y

        for section_index, lines in enumerate(
            wrapped_sections
        ):
            for line in lines:
                draw.text(
                    (x, current_y),
                    line,
                    font=font,
                    fill="black",
                )

                current_y += line_height

            if section_index < len(
                wrapped_sections
            ) - 1:
                current_y += section_spacing
