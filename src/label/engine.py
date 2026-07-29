from pathlib import Path

from PIL import Image
from PIL import ImageDraw

from .context import LabelContext
from .printer import BROTHER_QL600, Printer
from .style import LabelStyle
from .blocks.title_block import TitleBlock
from .blocks.country_block import CountryBlock
from .blocks.expiry_block import ExpiryBlock
from .blocks.ingredients_block import IngredientsBlock

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

    def render(
        self,
        product,
        output_path: str = "label_preview_new.png",
    ):
        width = self.context.printable_width_px

        margin_px = self.context.mm_to_px(
            self.context.style.margin_mm
        )

        min_height_px = self.context.mm_to_px(
            self.printer.min_length_mm
        )

        # imagine temporara pentru masurare
        temp_image = Image.new("RGB", (width, 2000), "white")
        temp_draw = ImageDraw.Draw(temp_image)

        title_block = TitleBlock(product, self.context)
        country_block = CountryBlock(product, self.context)
        expiry_block = ExpiryBlock(product, self.context)
        ingredients_block = IngredientsBlock(product, self.context)

        title_layout = title_block.measure(
            temp_draw,
            self.context
        )

        country_layout = country_block.measure(
            temp_draw,
            self.context
        )

        expiry_layout = expiry_block.measure(
            temp_draw,
            self.context
        )

        ingredients_layout = ingredients_block.measure(
            temp_draw,
            self.context
        )



        title_spacing_px = self.context.mm_to_px(
            self.context.style.title_spacing_mm
        )

        section_spacing_px = self.context.mm_to_px(
            self.context.style.section_spacing_mm
        )

        bottom_spacing_px = self.context.mm_to_px(
            self.context.style.bottom_spacing_mm
        )


        content_height = (
            margin_px
            + title_layout.height
            + title_spacing_px
            + country_layout.height
            + section_spacing_px
            + expiry_layout.height
            + section_spacing_px
            + ingredients_layout.height
            + bottom_spacing_px
            + margin_px
        )

        final_height = max(
            content_height,
            min_height_px
        )

        image = Image.new(
            "RGB",
            (width, final_height),
            "white"
        )

        draw = ImageDraw.Draw(image)

        current_y = margin_px

        title_block.render(
            draw=draw,
            x=margin_px,
            y=current_y,
            layout=title_layout,
            context=self.context,
        )

        current_y += title_layout.height
        current_y += title_spacing_px

        country_block.render(
            draw=draw,
            x=margin_px,
            y=current_y,
            layout=country_layout,
            context=self.context,
        )

        current_y += country_layout.height
        current_y += section_spacing_px

        expiry_block.render(
            draw=draw,
            x=margin_px,
            y=current_y,
            layout=expiry_layout,
            context=self.context,
        )

        current_y += expiry_layout.height
        current_y += section_spacing_px

        ingredients_block.render(
            draw=draw,
            x=margin_px,
            y=current_y,
            layout=ingredients_layout,
            context=self.context,
        )

        output = Path(output_path)
        image.save(output)

        print(f"[LABEL] {output}")