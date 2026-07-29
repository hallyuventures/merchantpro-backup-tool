from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout


class TextBlock(BaseBlock):

    def __init__(
        self,
        product,
        text: str,
        font_size: int,
        bold: bool = False,
        align: str = "left",
    ):
        super().__init__(product)

        self.text = text
        self.font_size = font_size
        self.bold = bold
        self.align = align

    def _load_font(self):
        font_name = "arialbd.ttf" if self.bold else "arial.ttf"

        try:
            return ImageFont.truetype(font_name, self.font_size)
        except OSError:
            return ImageFont.load_default()

    def _wrap_text(self, draw, text, font, max_width):
        words = text.split()

        if not words:
            return []

        lines = []
        current_line = words[0]

        for word in words[1:]:
            candidate = f"{current_line} {word}"

            left, top, right, bottom = draw.textbbox(
                (0, 0),
                candidate,
                font=font,
            )

            if right - left <= max_width:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        return lines

    def measure(self, context) -> BlockLayout:
        raise NotImplementedError(
            "TextBlock necesita un obiect ImageDraw pentru masurare."
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

        current_y = y

        for line in lines:
            draw.text(
                (x, current_y),
                line,
                font=font,
                fill="black",
                align=self.align,
            )

            current_y += line_height