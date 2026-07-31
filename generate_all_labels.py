from pathlib import Path
from tkinter import Tk, filedialog

from src.label.engine import LabelEngine
from src.product_json_loader import ProductJSONLoader
from src.product_validator import ProductValidator


def select_backup_folder() -> Path | None:
    root = Tk()
    root.withdraw()

    selected = filedialog.askdirectory(
        title="Selecteaza folderul backup MerchantPro"
    )

    root.destroy()

    if not selected:
        return None

    return Path(selected)


def main() -> None:
    backup_folder = select_backup_folder()

    if backup_folder is None:
        print("Operatie anulata.")
        return

    product_files = sorted(
        backup_folder.rglob("product.json")
    )

    if not product_files:
        print(
            "Nu am gasit niciun fisier product.json "
            f"in: {backup_folder}"
        )
        return

    output_folder = backup_folder / "_labels"
    output_folder.mkdir(exist_ok=True)

    engine = LabelEngine()

    generated = 0

    failed: list[tuple[Path, str]] = []

    warnings: list[
        tuple[int, str, list]
    ] = []

    print()
    print("=" * 60)
    print(" GENERATING LABELS")
    print("=" * 60)
    print()

    print(f"Produse gasite: {len(product_files)}")
    print(f"Destinatie: {output_folder}")
    print()

    for product_file in product_files:
        try:
            product = ProductJSONLoader.load(
                product_file
            )

            issues = ProductValidator.validate(
                product
            )

            if issues:
                warnings.append(
                    (
                        product.id,
                        product.name,
                        issues,
                    )
                )

            output_path = (
                output_folder
                / f"{product.id}.png"
            )

            engine.render(
                product,
                str(output_path),
            )

            generated += 1

            print(
                f"[OK] {product.id} - {product.name}"
            )

        except Exception as error:
            failed.append(
                (
                    product_file,
                    str(error),
                )
            )

            print(
                f"[ERROR] {product_file.parent.name}: "
                f"{error}"
            )

    print()
    print("=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    print()

    print(f"Etichete generate      : {generated}")
    print(f"Erori                  : {len(failed)}")
    print(f"Produse cu avertismente: {len(warnings)}")
    print(f"Folder                 : {output_folder}")

    if failed:
        error_report = (
            output_folder
            / "label_errors.txt"
        )

        with error_report.open(
            "w",
            encoding="utf-8",
        ) as file:
            for product_file, error in failed:
                file.write(
                    f"{product_file}\n"
                    f"{error}\n\n"
                )

        print()
        print(
            f"Raport erori: {error_report}"
        )

    if warnings:
        warning_report = (
            output_folder
            / "label_warnings.txt"
        )

        with warning_report.open(
            "w",
            encoding="utf-8",
        ) as file:
            for (
                product_id,
                product_name,
                issues,
            ) in warnings:
                file.write(
                    f"{product_id} - {product_name}\n"
                )

                for issue in issues:
                    file.write(
                        f"  [{issue.severity.upper()}] "
                        f"{issue.field}: "
                        f"{issue.message}\n"
                    )

                file.write("\n")

        print(
            f"Raport avertismente    : {warning_report}"
        )

    print()
    print("Done.")


if __name__ == "__main__":
    main()