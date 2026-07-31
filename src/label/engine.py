from pathlib import Path

from PIL import Image
from PIL import ImageDraw

from .context import LabelContext
from .printer import BROTHER_QL600, Printer
from .style import LabelStyle
from .blocks.title_block import TitleBlock
from .blocks.country_block import CountryBlock
from .blocks.ingredients_block import IngredientsBlock
from .blocks.allergens_block import AllergensBlock
from .blocks.usage_block import UsageBlock
from .blocks.extra_info_block import ExtraInfoBlock
from .blocks.nutrition_block import NutritionBlock
from .blocks.preparation_block import PreparationBlock
from .blocks.importer_block import ImporterBlock
from .blocks.alcohol_block import AlcoholBlock


class LabelEngine:

    def __init__(
        self,
        style: LabelStyle | None = None,
        printer: Printer = BROTHER_QL600,
    ):
        self.style = style or LabelStyle()
        self.printer = printer

        self.context = LabelContext(
            printer=self.printer,
            style=self.style,
        )

    def _build_blocks(self, product):
        title_spacing_px = self.context.mm_to_px(
            self.context.style.title_spacing_mm
        )

        section_spacing_px = self.context.mm_to_px(
            self.context.style.section_spacing_mm
        )

        return [
            (
                TitleBlock(product, self.context),
                title_spacing_px,
            ),
            (
                CountryBlock(product, self.context),
                section_spacing_px,
            ),
            (
                AlcoholBlock(product, self.context),
                section_spacing_px,
            ),
            (
                IngredientsBlock(product, self.context),
                section_spacing_px,
            ),
            (
                AllergensBlock(product, self.context),
                section_spacing_px,
            ),
            (
                NutritionBlock(product, self.context),
                section_spacing_px,
            ),
            (
                PreparationBlock(product, self.context),
                section_spacing_px,
            ),
            (
                UsageBlock(product, self.context),
                section_spacing_px,
            ),
            (
                ExtraInfoBlock(product, self.context),
                section_spacing_px,
            ),
            (
                ImporterBlock(product, self.context),
                0,
            ),
        ]

    def _measure(self, product):
        width = self.context.printable_width_px

        margin_px = self.context.mm_to_px(
            self.context.style.margin_mm
        )

        bottom_spacing_px = self.context.mm_to_px(
            self.context.style.bottom_spacing_mm
        )

        temp_image = Image.new(
            "RGB",
            (width, 4000),
            "white",
        )
        temp_draw = ImageDraw.Draw(temp_image)

        measured_blocks = []

        for block, spacing_after in self._build_blocks(product):
            layout = block.measure(
                temp_draw,
                self.context,
            )

            if layout.height == 0:
                continue

            measured_blocks.append(
                (
                    block,
                    layout,
                    spacing_after,
                )
            )

        if measured_blocks:
            last_block, last_layout, _ = measured_blocks[-1]

            measured_blocks[-1] = (
                last_block,
                last_layout,
                0,
            )

        content_height = (
            margin_px
            + sum(
                layout.height + spacing_after
                for _, layout, spacing_after in measured_blocks
            )
            + bottom_spacing_px
            + margin_px
        )

        return measured_blocks, content_height

    def measure_height_px(self, product) -> int:
        _, content_height = self._measure(product)

        min_height_px = self.context.mm_to_px(
            self.printer.min_length_mm
        )

        return max(
            content_height,
            min_height_px,
        )

    def measure_height_mm(self, product) -> float:
        height_px = self.measure_height_px(product)
        return height_px * 25.4 / self.printer.dpi

    def fits_length_mm(
        self,
        product,
        target_length_mm: float,
    ) -> bool:
        target_height_px = self.context.mm_to_px(
            target_length_mm
        )

        return self.measure_height_px(product) <= target_height_px

    def render(
        self,
        product,
        output_path: str = "label_preview_new.png",
        target_length_mm: float | None = None,
    ):
        width = self.context.printable_width_px

        margin_px = self.context.mm_to_px(
            self.context.style.margin_mm
        )

        measured_blocks, content_height = self._measure(product)

        min_height_px = self.context.mm_to_px(
            self.printer.min_length_mm
        )

        natural_height = max(
            content_height,
            min_height_px,
        )

        if target_length_mm is None:
            final_height = natural_height
        else:
            if target_length_mm < self.printer.min_length_mm:
                raise ValueError(
                    "Lungimea aleasa este mai mica decat "
                    f"minimul imprimantei: {self.printer.min_length_mm} mm."
                )

            final_height = self.context.mm_to_px(
                target_length_mm
            )

            if natural_height > final_height:
                required_mm = (
                    natural_height
                    * 25.4
                    / self.printer.dpi
                )

                raise ValueError(
                    "Continutul nu incape in lungimea aleasa. "
                    f"Sunt necesari aproximativ {required_mm:.1f} mm."
                )

        image = Image.new(
            "RGB",
            (width, final_height),
            "white",
        )

        draw = ImageDraw.Draw(image)
        current_y = margin_px

        for block, layout, spacing_after in measured_blocks:
            block.render(
                draw=draw,
                x=margin_px,
                y=current_y,
                layout=layout,
                context=self.context,
            )

            current_y += layout.height
            current_y += spacing_after

        output = Path(output_path)
        image.save(output)

        print(f"[LABEL] {output}")
