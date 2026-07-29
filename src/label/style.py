from dataclasses import dataclass


@dataclass
class LabelStyle:
    title_font_size: int = 16
    heading_font_size: int = 11
    body_font_size: int = 10

    margin_mm: float = 2.0
    padding_mm: float = 1.5

    section_spacing_mm: float = 2.0
    line_spacing_mm: float = 1.0