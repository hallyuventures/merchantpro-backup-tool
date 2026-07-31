import re

from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout


class IngredientsBlock(BaseBlock):

    INGREDIENTS_PATTERN = re.compile(
        r"^\s*ingrediente(?:\s*\(inci\))?\s*:\s*",
        flags=re.IGNORECASE,
    )

    INCI_PATTERN = re.compile(
        r"^\s*ingrediente\s*\(inci\)\s*:",
        flags=re.IGNORECASE,
    )

    ALLERGENS_PATTERN = re.compile(
        r"\b(?:alergeni|alergenii)\s*:\s*",
        flags=re.IGNORECASE,
    )

    def __init__(self, product, context):
        super().__init__(product)

        raw_text = str(
            product.ingredients or ""
        ).strip()

        self.ingredients_text = ""
        self.allergens_text = ""
        self.is_inci = False

        if raw_text:
            self._parse_text(raw_text)

        self.font_size = (
            context.style.body_font_size
        )

    def _parse_text(self, raw_text: str) -> None:
        cleaned = raw_text.strip()

        self.is_inci = False

        while cleaned:
            inci_match = re.match(
                r"^\s*ingrediente\s*\(inci\)\s*:\s*",
                cleaned,
                flags=re.IGNORECASE,
            )

            if inci_match:
                self.is_inci = True
                cleaned = cleaned[
                    inci_match.end():
                ].strip()
                continue

            ingredients_match = re.match(
                r"^\s*ingrediente\s*:\s*",
                cleaned,
                flags=re.IGNORECASE,
            )

            if ingredients_match:
                cleaned = cleaned[
                    ingredients_match.end():
                ].strip()
                continue

            break

        allergens_match = (
            self.ALLERGENS_PATTERN.search(cleaned)
        )

        if allergens_match is None:
            self.ingredients_text = cleaned.strip()
            return

        self.ingredients_text = cleaned[
            :allergens_match.start()
        ].strip(" \n\r\t.;")

        self.allergens_text = cleaned[
            allergens_match.end():
        ].strip()

    def _load_font(
        self,
        bold: bool = False,
    ):
        font_name = (
            "arialbd.ttf"
            if bold
            else "arial.ttf"
        )

        try:
            return ImageFont.truetype(
                font_name,
                self.font_size,
            )
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _wrap_text(
        draw,
        text: str,
        font,
        max_width: int,
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

            left, top, right, bottom = (
                draw.textbbox(
                    (0, 0),
                    candidate,
                    font=font,
                )
            )

            if right - left <= max_width:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        return lines

    @staticmethod
    def _font_height(
        draw,
        font,
    ) -> int:
        left, top, right, bottom = (
            draw.textbbox(
                (0, 0),
                "Ag",
                font=font,
            )
        )

        return bottom - top

    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        if (
            not self.ingredients_text
            and not self.allergens_text
        ):
            return BlockLayout(
                width=0,
                height=0,
                data={},
            )

        normal_font = self._load_font(
            bold=False
        )

        bold_font = self._load_font(
            bold=True
        )

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        max_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        heading = (
            "INGREDIENTE (INCI):"
            if self.is_inci
            else "INGREDIENTE:"
        )

        ingredients_full_text = ""

        if self.ingredients_text:
            ingredients_full_text = (
                f"{heading} "
                f"{self.ingredients_text}"
            )

        allergens_full_text = ""

        if self.allergens_text:
            allergens_full_text = (
                "ALERGENI: "
                f"{self.allergens_text}"
            )

        ingredients_lines = self._wrap_text(
            draw=draw,
            text=ingredients_full_text,
            font=normal_font,
            max_width=max_width,
        )

        allergens_lines = self._wrap_text(
            draw=draw,
            text=allergens_full_text,
            font=bold_font,
            max_width=max_width,
        )

        normal_height = self._font_height(
            draw,
            normal_font,
        )

        bold_height = self._font_height(
            draw,
            bold_font,
        )

        line_spacing = context.mm_to_px(
            context.style.line_spacing_mm
        )

        ingredients_height = 0

        if ingredients_lines:
            ingredients_height = (
                len(ingredients_lines)
                * normal_height
                + (
                    len(ingredients_lines) - 1
                )
                * line_spacing
            )

        allergens_height = 0

        if allergens_lines:
            allergens_height = (
                len(allergens_lines)
                * bold_height
                + (
                    len(allergens_lines) - 1
                )
                * line_spacing
            )

        section_spacing = 0

        if ingredients_lines and allergens_lines:
            section_spacing = line_spacing

        total_height = (
            ingredients_height
            + section_spacing
            + allergens_height
        )

        return BlockLayout(
            width=max_width,
            height=total_height,
            data={
                "normal_font": normal_font,
                "bold_font": bold_font,
                "ingredients_lines": (
                    ingredients_lines
                ),
                "allergens_lines": (
                    allergens_lines
                ),
                "normal_line_height": (
                    normal_height
                    + line_spacing
                ),
                "bold_line_height": (
                    bold_height
                    + line_spacing
                ),
                "ingredients_height": (
                    ingredients_height
                ),
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
        if layout.height == 0:
            return

        current_y = y

        normal_font = layout.data[
            "normal_font"
        ]

        bold_font = layout.data[
            "bold_font"
        ]

        for line in layout.data[
            "ingredients_lines"
        ]:
            draw.text(
                (x, current_y),
                line,
                font=normal_font,
                fill="black",
            )

            current_y += layout.data[
                "normal_line_height"
            ]

        if (
            layout.data["ingredients_lines"]
            and layout.data["allergens_lines"]
        ):
            current_y = (
                y
                + layout.data[
                    "ingredients_height"
                ]
                + layout.data[
                    "section_spacing"
                ]
            )

        for line in layout.data[
            "allergens_lines"
        ]:
            draw.text(
                (x, current_y),
                line,
                font=bold_font,
                fill="black",
            )

            current_y += layout.data[
                "bold_line_height"
            ]