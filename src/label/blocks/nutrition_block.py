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

    @staticmethod
    def _text_width(draw, text, font) -> int:
        if not text:
            return 0

        left, top, right, bottom = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )
        return right - left

    def _wrap_text(
        self,
        draw,
        text: str,
        font,
        max_width: int,
    ) -> list[str]:
        text = (text or "").strip()

        if not text:
            return []

        if max_width <= 0:
            return [text]

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

    def _lines_height(
        self,
        line_count: int,
        text_height: int,
        line_spacing: int,
    ) -> int:
        if line_count <= 0:
            return 0

        return (
            line_count * text_height
            + (line_count - 1) * line_spacing
        )

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

        line_spacing_px = context.mm_to_px(
            context.style.line_spacing_mm
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

        value_column_width = max(
            1,
            values_width // column_count
        )

        label_text_width = max(
            1,
            label_column_width - 2 * padding_px
        )

        value_text_width = max(
            1,
            value_column_width - 2 * padding_px
        )

        title_lines = self._wrap_text(
            draw,
            "VALORI NUTRITIONALE TIPICE",
            header_font,
            label_text_width,
        )

        header_lines_per_column: list[list[str]] = []

        for index in range(column_count):
            header = ""

            if index < len(self.nutrition.headers):
                header = self.nutrition.headers[index]

            wrapped = self._wrap_text(
                draw,
                header,
                header_font,
                value_text_width,
            )

            header_lines_per_column.append(wrapped)

        header_line_count = max(
            [len(title_lines)]
            + [
                len(lines)
                for lines in header_lines_per_column
            ]
        )

        header_row_height = (
            self._lines_height(
                header_line_count,
                header_text_height,
                line_spacing_px,
            )
            + 2 * padding_px
        )

        measured_rows: list[dict] = []

        for row in self.nutrition.rows:
            label_lines = self._wrap_text(
                draw,
                row.label,
                body_font,
                label_text_width,
            )

            value_lines_per_column: list[list[str]] = []

            for index in range(column_count):
                value = ""

                if index < len(row.values):
                    value = row.values[index]

                wrapped = self._wrap_text(
                    draw,
                    value,
                    body_font,
                    value_text_width,
                )

                value_lines_per_column.append(wrapped)

            row_line_count = max(
                [len(label_lines)]
                + [
                    len(lines)
                    for lines in value_lines_per_column
                ]
            )

            row_height = (
                self._lines_height(
                    row_line_count,
                    body_text_height,
                    line_spacing_px,
                )
                + 2 * padding_px
            )

            measured_rows.append(
                {
                    "label_lines": label_lines,
                    "value_lines_per_column": value_lines_per_column,
                    "row_height": row_height,
                }
            )

        total_height = (
            header_row_height
            + sum(
                row["row_height"]
                for row in measured_rows
            )
        )

        return BlockLayout(
            width=table_width,
            height=total_height,
            data={
                "body_font": body_font,
                "header_font": header_font,
                "padding_px": padding_px,
                "line_spacing_px": line_spacing_px,
                "body_text_height": body_text_height,
                "header_text_height": header_text_height,
                "header_row_height": header_row_height,
                "column_count": column_count,
                "label_column_width": label_column_width,
                "value_column_width": value_column_width,
                "title_lines": title_lines,
                "header_lines_per_column": header_lines_per_column,
                "measured_rows": measured_rows,
            },
        )

    def _draw_lines(
        self,
        draw,
        x: int,
        y: int,
        lines: list[str],
        font,
        text_height: int,
        line_spacing: int,
    ) -> None:
        current_y = y

        for line in lines:
            draw.text(
                (x, current_y),
                line,
                font=font,
                fill="black",
            )
            current_y += text_height + line_spacing

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
        line_spacing_px = data["line_spacing_px"]

        body_text_height = data["body_text_height"]
        header_text_height = data["header_text_height"]

        header_row_height = data[
            "header_row_height"
        ]

        column_count = data["column_count"]
        label_column_width = data[
            "label_column_width"
        ]
        value_column_width = data[
            "value_column_width"
        ]

        title_lines = data["title_lines"]
        header_lines_per_column = data[
            "header_lines_per_column"
        ]
        measured_rows = data["measured_rows"]

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

        self._draw_lines(
            draw=draw,
            x=x + padding_px,
            y=current_y + padding_px,
            lines=title_lines,
            font=header_font,
            text_height=header_text_height,
            line_spacing=line_spacing_px,
        )

        for index in range(column_count):
            header_lines = header_lines_per_column[index]

            self._draw_lines(
                draw=draw,
                x=(
                    values_x
                    + index * value_column_width
                    + padding_px
                ),
                y=current_y + padding_px,
                lines=header_lines,
                font=header_font,
                text_height=header_text_height,
                line_spacing=line_spacing_px,
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

        for row_data in measured_rows:
            row_height = row_data["row_height"]

            self._draw_lines(
                draw=draw,
                x=x + padding_px,
                y=current_y + padding_px,
                lines=row_data["label_lines"],
                font=body_font,
                text_height=body_text_height,
                line_spacing=line_spacing_px,
            )

            for index in range(column_count):
                value_lines = row_data[
                    "value_lines_per_column"
                ][index]

                self._draw_lines(
                    draw=draw,
                    x=(
                        values_x
                        + index * value_column_width
                        + padding_px
                    ),
                    y=current_y + padding_px,
                    lines=value_lines,
                    font=body_font,
                    text_height=body_text_height,
                    line_spacing=line_spacing_px,
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

        for index in range(1, column_count):
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