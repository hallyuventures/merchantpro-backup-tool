print("1. Script pornit")

from src.label.windows_printer import WindowsLabelPrinter

print("2. Import reusit")

printer = WindowsLabelPrinter(
    printer_name="Brother QL-600",
)

print("3. Obiect printer creat")

printer.print_image(
    "label_full_test.png",
)

print("4. Comanda de print terminata")