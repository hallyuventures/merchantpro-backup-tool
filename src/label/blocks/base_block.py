from abc import ABC, abstractmethod

from ..layout import BlockLayout


class BaseBlock(ABC):

    def __init__(self, product):
        self.product = product

    @abstractmethod
    def measure(self, draw, context) -> BlockLayout:
        """Calculeaza si returneaza layout-ul blocului."""
        font = self._load_font()

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        max_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        lines = self._wrap_text(
            draw=draw,
            text=self.text,
            font=font,
            max_width=max_width,
        )

        left, top, right, bottom = draw.textbbox(
            (0, 0),
            "Ag",
            font=font,
        )

        text_height = bottom - top

        line_spacing = context.mm_to_px(
            context.style.line_spacing_mm
        )

        line_height = text_height + line_spacing

        if lines:
            height = (
                len(lines) * text_height
                + (len(lines) - 1) * line_spacing
            )
        else:
            height = 0

        return BlockLayout(
            width=max_width,
            height=height,
            data={
                "font": font,
                "lines": lines,
                "line_height": line_height,
            },
        )
    
    @abstractmethod
    def render(
        self,
        draw,
        x: int,
        y: int,
        layout: BlockLayout,
        context,
    ) -> None:
        """Deseneaza blocul folosind layout-ul deja calculat."""
        raise NotImplementedError