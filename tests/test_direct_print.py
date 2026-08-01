import sys
from pathlib import Path

print("1. Script pornit")

from src.label.windows_printer import WindowsLabelPrinter

print("2. Import reusit")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "Utilizare:\n"
            "py -m tests.test_direct_print "
            r'"cale\catre\eticheta.png"'
        )

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        raise FileNotFoundError(
            f"Imaginea nu exista: {image_path}"
        )

    printer = WindowsLabelPrinter(
        printer_name="Brother QL-600",
    )

    print("3. Obiect printer creat")
    print(f"4. Tiparesc: {image_path}")

    printer.print_image(image_path)

    print("5. Comanda de print terminata")


if __name__ == "__main__":
    main()