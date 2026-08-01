from pathlib import Path

from PIL import Image
from PIL import ImageWin

import win32con
import win32gui
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

        with Image.open(image_path) as source:
            image = source.convert("RGB")

        label_length_mm = (
            image.height * 25.4 / self.dpi
        )

        printer_handle = win32print.OpenPrinter(
            self.printer_name
        )

        printer_dc = None
        hdc = None

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

            devmode.Orientation = win32con.DMORIENT_PORTRAIT

            devmode.Fields |= (
                win32con.DM_PAPERSIZE
                | win32con.DM_PAPERWIDTH
                | win32con.DM_PAPERLENGTH
                | win32con.DM_ORIENTATION
            )

            # Creeaza DC-ul folosind explicit configuratia custom.
            hdc = win32gui.CreateDC(
                "WINSPOOL",
                self.printer_name,
                None,
            )

            hdc = win32gui.ResetDC(
                hdc,
                devmode,
            )
            
            printer_dc = win32ui.CreateDCFromHandle(
                hdc
            )

            printable_width = printer_dc.GetDeviceCaps(
                win32con.HORZRES
            )
            printable_height = printer_dc.GetDeviceCaps(
                win32con.VERTRES
            )

            width_difference = abs(
                printable_width - image.width
            )

            if width_difference > 5:
                raise ValueError(
                    "Latimea PNG-ului nu corespunde cu "
                    "latimea imprimabila a driverului. "
                    f"PNG: {image.width}px; "
                    f"driver: {printable_width}px."
                )

            # Nu redimensionam imaginea. O centram doar daca
            # driverul raporteaza o diferenta de cativa pixeli.
            x = max(
                0,
                (printable_width - image.width) // 2,
            )
            y = 0

            target_width = image.width
            target_height = min(
                image.height,
                printable_height,
            )

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

        finally:
            if printer_dc is not None:
                printer_dc.DeleteDC()

            # CreateDCFromHandle preia gestionarea handle-ului;
            # nu apelam DeleteDC separat asupra aceluiasi HDC.
            win32print.ClosePrinter(
                printer_handle
            )
