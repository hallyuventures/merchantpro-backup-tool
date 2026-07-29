from .context import LabelContext
from .printer import BROTHER_QL600, Printer
from .style import LabelStyle


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