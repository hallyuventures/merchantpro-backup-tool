from dataclasses import dataclass


@dataclass(frozen=True)
class Printer:
    label_width_mm: float
    printable_width_mm: float
    min_length_mm: float
    dpi: int


BROTHER_QL600 = Printer(
    label_width_mm=62.0,
    printable_width_mm=59.0,
    min_length_mm=12.7,
    dpi=300,
)