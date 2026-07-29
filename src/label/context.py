from .printer import Printer
from .style import LabelStyle


class LabelContext:

    def __init__(self, printer: Printer, style: LabelStyle):
        self.printer = printer
        self.style = style

    def mm_to_px(self, mm: float) -> int:
        return round(mm * self.printer.dpi / 25.4)

    @property
    def printable_width_px(self) -> int:
        return self.mm_to_px(self.printer.printable_width_mm)