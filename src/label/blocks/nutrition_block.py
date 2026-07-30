from PIL import ImageFont

from .base_block import BaseBlock
from ..layout import BlockLayout
from ..nutrition_parser import NutritionParser


class NutritionBlock(BaseBlock):

    def __init__(self, product, context):
        super().__init__(product)

        self.nutrition = NutritionParser.parse(
            product.nutrition
        )

        self.body_font_size = (
            context.style.nutrition_font_size
        )

    def _load_font(
        self,
        font_size: int,
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
                font_size,
            )
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _text_height(draw, font) -> int:
        left, top, right, bottom = draw.textbbox(
            (0, 0),
            "Ag",
            font=font,
        )

        return bottom - top

    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        if self.nutrition.is_empty:
            return BlockLayout(
                width=0,
                height=0,
            )

        margin_px = context.mm_to_px(
            context.style.margin_mm
        )

        table_width = (
            context.printable_width_px
            - 2 * margin_px
        )

        padding_px = context.mm_to_px(
            context.style.nutrition_padding_mm
        )

        body_font = self._load_font(
            self.body_font_size,
        )

        header_font = self._load_font(
            self.body_font_size,
            bold=True,
        )

        body_text_height = self._text_height(
            draw,
            body_font,
        )

        header_text_height = self._text_height(
            draw,
            header_font,
        )

        column_count = max(
            1,
            max(
                (
                    len(row.values)
                    for row in self.nutrition.rows
                ),
                default=1,
            ),
            len(self.nutrition.headers),
        )

        label_column_width = round(
            table_width * 0.46
        )

        values_width = (
            table_width
            - label_column_width
        )

        value_column_width = (
            values_width // column_count
        )

        header_row_height = (
            header_text_height
            + 2 * padding_px
        )

        row_height = (
            body_text_height
            + 2 * padding_px
        )

        total_height = (
            header_row_height
            + len(self.nutrition.rows) * row_height
        )

        return BlockLayout(
            width=table_width,
            height=total_height,
            data={
                "body_font": body_font,
                "header_font": header_font,
                "padding_px": padding_px,
                "header_row_height": header_row_height,
                "row_height": row_height,
                "column_count": column_count,
                "label_column_width": label_column_width,
                "value_column_width": value_column_width,
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

        data = layout.data

        body_font = data["body_font"]
        header_font = data["header_font"]

        padding_px = data["padding_px"]
        header_row_height = data[
            "header_row_height"
        ]
        row_height = data["row_height"]

        column_count = data["column_count"]
        label_column_width = data[
            "label_column_width"
        ]
        value_column_width = data[
            "value_column_width"
        ]

        table_right = x + layout.width
        table_bottom = y + layout.height

        values_x = x + label_column_width
        current_y = y

        draw.rectangle(
            (
                x,
                y,
                table_right,
                table_bottom,
            ),
            outline="black",
            width=1,
        )

        draw.text(
            (
                x + padding_px,
                current_y + padding_px,
            ),
            "VALORI NUTRITIONALE TIPICE",
            font=header_font,
            fill="black",
        )

        for index in range(column_count):
            header = ""

            if index < len(
                self.nutrition.headers
            ):
                header = (
                    self.nutrition
                    .headers[index]
                )

            draw.text(
                (
                    values_x
                    + index * value_column_width
                    + padding_px,
                    current_y + padding_px,
                ),
                header,
                font=header_font,
                fill="black",
            )

        current_y += header_row_height

        draw.line(
            (
                x,
                current_y,
                table_right,
                current_y,
            ),
            fill="black",
            width=1,
        )

        for row in self.nutrition.rows:
            draw.text(
                (
                    x + padding_px,
                    current_y + padding_px,
                ),
                row.label,
                font=body_font,
                fill="black",
            )

            for index in range(column_count):
                value = ""

                if index < len(row.values):
                    value = row.values[index]

                draw.text(
                    (
                        values_x
                        + index * value_column_width
                        + padding_px,
                        current_y + padding_px,
                    ),
                    value,
                    font=body_font,
                    fill="black",
                )

            current_y += row_height

            draw.line(
                (
                    x,
                    current_y,
                    table_right,
                    current_y,
                ),
                fill="black",
                width=1,
            )

        separator_x = x + label_column_width

        draw.line(
            (
                separator_x,
                y,
                separator_x,
                table_bottom,
            ),
            fill="black",
            width=1,
        )

        for index in range(
            1,
            column_count,
        ):
            separator_x = (
                x
                + label_column_width
                + index * value_column_width
            )

            draw.line(
                (
                    separator_x,
                    y,
                    separator_x,
                    table_bottom,
                ),
                fill="black",
                width=1,
            )