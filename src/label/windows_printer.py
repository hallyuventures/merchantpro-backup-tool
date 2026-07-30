from pathlib import Path

from PIL import Image
from PIL import ImageWin

import win32con
import win32print
import win32ui


class WindowsLabelPrinter:

    def __init__(
        self,
        printer_name: str = "Brother QL-600",
        media_width_mm: float = 62.0,
        dpi: int = 300,
    ):
        self.printer_name = printer_name
        self.media_width_mm = media_width_mm
        self.dpi = dpi

    def print_image(
        self,
        image_path: str | Path,
        job_name: str = "K-Goodies Label",
    ) -> None:
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Imaginea nu exista: {image_path}"
            )

        image = Image.open(image_path).convert("RGB")

        label_length_mm = (
            image.height * 25.4 / self.dpi
        )

        printer_handle = win32print.OpenPrinter(
            self.printer_name
        )

        try:
            printer_info = win32print.GetPrinter(
                printer_handle,
                2,
            )

            devmode = printer_info["pDevMode"]

            devmode.PaperSize = win32con.DMPAPER_USER
            devmode.PaperWidth = round(
                self.media_width_mm * 10
            )
            devmode.PaperLength = round(
                label_length_mm * 10
            )

            devmode.Fields |= (
                win32con.DM_PAPERSIZE
                | win32con.DM_PAPERWIDTH
                | win32con.DM_PAPERLENGTH
            )

            printer_dc = win32ui.CreateDC()
            printer_dc.CreatePrinterDC(
                self.printer_name
            )

            printable_width = printer_dc.GetDeviceCaps(
                win32con.HORZRES
            )
            printable_height = printer_dc.GetDeviceCaps(
                win32con.VERTRES
            )

            physical_width = printer_dc.GetDeviceCaps(
                win32con.PHYSICALWIDTH
            )
            physical_offset_x = printer_dc.GetDeviceCaps(
                win32con.PHYSICALOFFSETX
            )
            physical_offset_y = printer_dc.GetDeviceCaps(
                win32con.PHYSICALOFFSETY
            )

            scale = min(
                printable_width / image.width,
                printable_height / image.height,
            )

            target_width = round(
                image.width * scale
            )
            target_height = round(
                image.height * scale
            )

            x = max(
                physical_offset_x,
                (
                    physical_width
                    - target_width
                ) // 2,
            )

            y = physical_offset_y

            dib = ImageWin.Dib(image)

            printer_dc.StartDoc(job_name)
            printer_dc.StartPage()

            dib.draw(
                printer_dc.GetHandleOutput(),
                (
                    x,
                    y,
                    x + target_width,
                    y + target_height,
                ),
            )

            printer_dc.EndPage()
            printer_dc.EndDoc()
            printer_dc.DeleteDC()

        finally:
            win32print.ClosePrinter(
                printer_handle
            )