from pathlib import Path
from tkinter import Tk, filedialog


def select_excel_file(title: str) -> Path | None:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    filename = filedialog.askopenfilename(
        title=title,
        filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*"),
        ],
    )

    root.destroy()

    if not filename:
        return None

    return Path(filename)