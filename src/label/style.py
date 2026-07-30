from dataclasses import dataclass


@dataclass
class LabelStyle:
    title_font_size: int = 24
    heading_font_size: int = 16
    body_font_size: int = 17
    nutrition_font_size: int = 17

    margin_mm: float = 0.5
    padding_mm: float = 1.5
    nutrition_padding_mm: float = 0.5

    title_spacing_mm: float = 1.5
    section_spacing_mm: float = 0.5
    bottom_spacing_mm: float = 0.2
    line_spacing_mm: float = 0.3