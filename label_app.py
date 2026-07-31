import json
import os
import re
from pathlib import Path
from tkinter import (
    BOTH,
    END,
    LEFT,
    RIGHT,
    StringVar,
    Tk,
    Toplevel,
    filedialog,
    messagebox,
)
from tkinter import ttk

from src.label.engine import LabelEngine
from src.operator_registry import OperatorRegistry
from src.product_json_loader import ProductJSONLoader
from src.product_operator_registry import (
    ProductOperatorRegistry,
)


class LabelApp:

    def __init__(self, root: Tk):
        self.root = root
        self.root.title("K-Goodies Label Tool")
        self.root.geometry("860x520")

        self.backup_folder = Path("backup")
        self.current_product = None
        self.product_files: dict[int, Path] = {}

        self.operator_registry = OperatorRegistry(
            "data/operators.json"
        )
        self.operator_registry.load()

        self.assignment_registry = (
            ProductOperatorRegistry(
                "data/product_operators.json"
            )
        )
        self.assignment_registry.load()

        self.operator_name_to_id: dict[str, str] = {}

        self.product_id_var = StringVar()
        self.product_name_var = StringVar(
            value="Niciun produs incarcat"
        )
        self.supplier_var = StringVar(
            value="-"
        )
        self.operator_var = StringVar()
        self.distributor_var = StringVar()
        self.status_var = StringVar(
            value="Selecteaza folderul de backup."
        )

        self._build_ui()
        self._refresh_operator_dropdowns()
        self._index_products()

    def _build_ui(self) -> None:
        container = ttk.Frame(
            self.root,
            padding=16,
        )
        container.pack(
            fill=BOTH,
            expand=True,
        )

        backup_frame = ttk.Frame(container)
        backup_frame.pack(
            fill="x",
            pady=(0, 15),
        )

        ttk.Button(
            backup_frame,
            text="Selecteaza backup",
            command=self.select_backup_folder,
        ).pack(side=LEFT)

        self.backup_label = ttk.Label(
            backup_frame,
            text=str(self.backup_folder),
        )
        self.backup_label.pack(
            side=LEFT,
            padx=12,
        )

        product_frame = ttk.LabelFrame(
            container,
            text="Produs",
            padding=12,
        )
        product_frame.pack(
            fill="x",
            pady=(0, 12),
        )

        ttk.Label(
            product_frame,
            text="ID produs:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        product_entry = ttk.Entry(
            product_frame,
            textvariable=self.product_id_var,
            width=15,
        )
        product_entry.grid(
            row=0,
            column=1,
            padx=8,
            sticky="w",
        )
        product_entry.bind(
            "<Return>",
            lambda event: self.load_product(),
        )

        ttk.Button(
            product_frame,
            text="Incarca",
            command=self.load_product,
        ).grid(
            row=0,
            column=2,
            sticky="w",
        )

        ttk.Label(
            product_frame,
            text="Denumire:",
        ).grid(
            row=1,
            column=0,
            pady=(12, 0),
            sticky="nw",
        )

        ttk.Label(
            product_frame,
            textvariable=self.product_name_var,
            wraplength=580,
        ).grid(
            row=1,
            column=1,
            columnspan=3,
            pady=(12, 0),
            sticky="w",
        )

        ttk.Label(
            product_frame,
            text="Furnizor:",
        ).grid(
            row=2,
            column=0,
            pady=(8, 0),
            sticky="w",
        )

        ttk.Label(
            product_frame,
            textvariable=self.supplier_var,
        ).grid(
            row=2,
            column=1,
            columnspan=3,
            pady=(8, 0),
            sticky="w",
        )

        operator_frame = ttk.LabelFrame(
            container,
            text="Date juridice pentru eticheta",
            padding=12,
        )
        operator_frame.pack(
            fill="x",
            pady=(0, 12),
        )

        ttk.Label(
            operator_frame,
            text="Operator / Importator:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.operator_combo = ttk.Combobox(
            operator_frame,
            textvariable=self.operator_var,
            state="readonly",
            width=55,
        )
        self.operator_combo.grid(
            row=0,
            column=1,
            padx=8,
            sticky="ew",
        )

        ttk.Button(
            operator_frame,
            text="Adauga operator",
            command=lambda: self.open_add_operator_dialog(
                target="operator"
            ),
        ).grid(
            row=0,
            column=2,
            padx=(8, 0),
        )

        ttk.Label(
            operator_frame,
            text="Distribuitor:",
        ).grid(
            row=1,
            column=0,
            pady=(12, 0),
            sticky="w",
        )

        self.distributor_combo = ttk.Combobox(
            operator_frame,
            textvariable=self.distributor_var,
            state="readonly",
            width=55,
        )
        self.distributor_combo.grid(
            row=1,
            column=1,
            padx=8,
            pady=(12, 0),
            sticky="ew",
        )

        ttk.Button(
            operator_frame,
            text="Adauga distribuitor",
            command=lambda: self.open_add_operator_dialog(
                target="distributor"
            ),
        ).grid(
            row=1,
            column=2,
            padx=(8, 0),
            pady=(12, 0),
        )

        ttk.Button(
            operator_frame,
            text="Salveaza asocierea",
            command=self.save_assignment,
        ).grid(
            row=2,
            column=1,
            pady=(12, 0),
            sticky="w",
        )

        operator_frame.columnconfigure(
            1,
            weight=1,
        )

        action_frame = ttk.Frame(container)
        action_frame.pack(
            fill="x",
            pady=(4, 0),
        )

        ttk.Button(
            action_frame,
            text="Genereaza preview",
            command=self.generate_preview,
        ).pack(side=LEFT)

        ttk.Label(
            action_frame,
            textvariable=self.status_var,
        ).pack(
            side=RIGHT,
            padx=8,
        )

    def select_backup_folder(self) -> None:
        selected = filedialog.askdirectory(
            title="Selecteaza folderul backup"
        )

        if not selected:
            return

        self.backup_folder = Path(selected)
        self.backup_label.configure(
            text=str(self.backup_folder)
        )

        self._index_products()

    def _index_products(self) -> None:
        self.product_files = {}

        if not self.backup_folder.exists():
            self.status_var.set(
                "Folderul backup nu exista."
            )
            return

        for product_file in self.backup_folder.rglob(
            "product.json"
        ):
            try:
                with product_file.open(
                    "r",
                    encoding="utf-8",
                ) as file:
                    data = json.load(file)

                product_id = int(data["id"])
                self.product_files[
                    product_id
                ] = product_file

            except (
                OSError,
                ValueError,
                KeyError,
                json.JSONDecodeError,
            ):
                continue

        self.status_var.set(
            f"{len(self.product_files)} produse indexate."
        )

    def _refresh_operator_dropdowns(self) -> None:
        self.operator_name_to_id = {}

        names: list[str] = []

        for operator_id, operator in sorted(
            self.operator_registry.operators.items(),
            key=lambda item: str(
                item[1].get(
                    "display_name",
                    item[0],
                )
            ).lower(),
        ):
            display_name = str(
                operator.get(
                    "display_name",
                    operator_id,
                )
            ).strip()

            label = (
                f"{display_name} [{operator_id}]"
            )

            names.append(label)
            self.operator_name_to_id[
                label
            ] = operator_id

        self.operator_combo[
            "values"
        ] = names
        self.distributor_combo[
            "values"
        ] = names

    def load_product(self) -> None:
        raw_id = self.product_id_var.get().strip()

        try:
            product_id = int(raw_id)
        except ValueError:
            messagebox.showerror(
                "ID invalid",
                "Introdu un ID numeric.",
            )
            return

        product_file = self.product_files.get(
            product_id
        )

        if product_file is None:
            messagebox.showerror(
                "Produs negasit",
                f"Nu am gasit produsul {product_id} "
                "in backup.",
            )
            return

        try:
            self.current_product = (
                ProductJSONLoader.load(
                    product_file
                )
            )
        except Exception as error:
            messagebox.showerror(
                "Eroare",
                str(error),
            )
            return

        self.product_name_var.set(
            self.current_product.name
        )

        self.supplier_var.set(
            self.current_product.supplier
            or "Furnizor necompletat"
        )

        self._preselect_operator(
            product_id
        )

        self.status_var.set(
            f"Produs {product_id} incarcat."
        )

    def _preselect_operator(
        self,
        product_id: int,
    ) -> None:
        operator_id = (
            self.assignment_registry
            .get_responsible_operator_id(
                product_id
            )
        )

        distributor_id = (
            self.assignment_registry
            .get_distributor_id(
                product_id
            )
        )

        self.operator_var.set("")
        self.distributor_var.set("")

        if operator_id:
            self._select_id(
                operator_id,
                self.operator_var,
            )

        if distributor_id:
            self._select_id(
                distributor_id,
                self.distributor_var,
            )
            return

        supplier = str(
            self.current_product.supplier or ""
        ).strip()

        distributor_id = (
            self._find_operator_by_name(
                supplier
            )
        )

        if distributor_id:
            self._select_id(
                distributor_id,
                self.distributor_var,
            )

    def _select_id(
        self,
        operator_id: str,
        variable: StringVar,
    ) -> None:
        for label, current_id in (
            self.operator_name_to_id.items()
        ):
            if current_id == operator_id:
                variable.set(label)
                return

    def _selected_id(
        self,
        variable: StringVar,
    ) -> str:
        selected_label = variable.get().strip()

        return self.operator_name_to_id.get(
            selected_label,
            "",
        )

    def _find_operator_by_name(
        self,
        company_name: str,
    ) -> str:
        target = self._company_key(
            company_name
        )

        if not target:
            return ""

        for operator_id, operator in (
            self.operator_registry.operators.items()
        ):
            display_name = str(
                operator.get("display_name", "")
            )

            if self._company_key(display_name) == target:
                return operator_id

        return ""

    @staticmethod
    def _company_key(value: str) -> str:
        value = value.lower().strip()

        replacements = {
            "ă": "a",
            "â": "a",
            "î": "i",
            "ș": "s",
            "ş": "s",
            "ț": "t",
            "ţ": "t",
        }

        for source, target in replacements.items():
            value = value.replace(source, target)

        value = re.sub(
            r"\b(srl|sa|gmbh|b\.?v\.?|inc)\b",
            "",
            value,
            flags=re.IGNORECASE,
        )

        return re.sub(
            r"[^a-z0-9]+",
            "",
            value,
        )

    def save_assignment(self) -> bool:
        if self.current_product is None:
            messagebox.showwarning(
                "Produs lipsa",
                "Incarca mai intai un produs.",
            )
            return False

        operator_id = self._selected_id(
            self.operator_var
        )

        distributor_id = self._selected_id(
            self.distributor_var
        )

        if not operator_id:
            messagebox.showwarning(
                "Operator lipsa",
                "Selecteaza un operator.",
            )
            return False

        if not distributor_id:
            messagebox.showwarning(
                "Distribuitor lipsa",
                "Selecteaza un distribuitor.",
            )
            return False

        self.assignment_registry.set_assignment(
            product_id=self.current_product.id,
            responsible_operator_id=operator_id,
            distributor_id=distributor_id,
        )

        self.status_var.set(
            "Asocierea a fost salvata."
        )

        return True

    def generate_preview(self) -> None:
        if self.current_product is None:
            messagebox.showwarning(
                "Produs lipsa",
                "Incarca mai intai un produs.",
            )
            return

        operator_id = self._selected_id(
            self.operator_var
        )

        distributor_id = self._selected_id(
            self.distributor_var
        )

        if not operator_id:
            messagebox.showwarning(
                "Operator lipsa",
                "Selecteaza operatorul/importatorul.",
            )
            return

        if not distributor_id:
            messagebox.showwarning(
                "Distribuitor lipsa",
                "Selecteaza distribuitorul.",
            )
            return

        self.assignment_registry.set_assignment(
            product_id=self.current_product.id,
            responsible_operator_id=operator_id,
            distributor_id=distributor_id,
        )

        self.current_product.importer_distributor = (
            self._build_legal_text(
                operator_id,
                distributor_id,
            )
        )

        output_folder = (
            self.backup_folder
            / "_label_preview"
        )
        output_folder.mkdir(
            exist_ok=True
        )

        output_path = (
            output_folder
            / f"{self.current_product.id}.png"
        )

        try:
            LabelEngine().render(
                self.current_product,
                str(output_path),
            )
        except Exception as error:
            messagebox.showerror(
                "Eroare generare",
                str(error),
            )
            return

        self.status_var.set(
            f"Preview generat: {output_path.name}"
        )

        if os.name == "nt":
            os.startfile(output_path)
        else:
            messagebox.showinfo(
                "Preview generat",
                str(output_path),
            )

    def _build_legal_text(
        self,
        operator_id: str,
        distributor_id: str,
    ) -> str:
        if operator_id == distributor_id:
            return self._format_entity(
                operator_id,
                "IMPORTATOR SI DISTRIBUITOR IN ROMANIA",
            )

        operator_text = self._format_entity(
            operator_id,
            "OPERATOR RESPONSABIL / IMPORTATOR IN UE",
        )

        distributor_text = self._format_entity(
            distributor_id,
            "DISTRIBUITOR IN ROMANIA",
        )

        return f"{operator_text}\n{distributor_text}"

    def _format_entity(
        self,
        operator_id: str,
        role_label: str,
    ) -> str:
        operator = self.operator_registry.require(
            operator_id
        )

        display_name = str(
            operator.get("display_name", "")
        ).strip()

        address = self.operator_registry.format_address(
            operator_id
        )

        parts = [
            f"{role_label}:",
            display_name,
        ]

        if address:
            parts.append(address)

        return " ".join(parts)

    def open_add_operator_dialog(
        self,
        target: str,
    ) -> None:
        dialog = Toplevel(self.root)
        dialog.title(
            "Adauga operator"
            if target == "operator"
            else "Adauga distribuitor"
        )
        dialog.geometry("520x390")
        dialog.transient(self.root)
        dialog.grab_set()

        fields = {
            "display_name": StringVar(),
            "street": StringVar(),
            "postal_code": StringVar(),
            "city": StringVar(),
            "country": StringVar(),
        }

        labels = [
            ("Denumire firma", "display_name"),
            ("Strada", "street"),
            ("Cod postal", "postal_code"),
            ("Localitate", "city"),
            ("Tara", "country"),
        ]

        frame = ttk.Frame(
            dialog,
            padding=16,
        )
        frame.pack(
            fill=BOTH,
            expand=True,
        )

        for row_index, (
            label_text,
            field_name,
        ) in enumerate(labels):
            ttk.Label(
                frame,
                text=label_text,
            ).grid(
                row=row_index,
                column=0,
                pady=6,
                sticky="w",
            )

            ttk.Entry(
                frame,
                textvariable=fields[field_name],
                width=42,
            ).grid(
                row=row_index,
                column=1,
                pady=6,
                padx=8,
                sticky="ew",
            )

        def save_operator() -> None:
            display_name = fields[
                "display_name"
            ].get().strip()

            if not display_name:
                messagebox.showwarning(
                    "Denumire lipsa",
                    "Completeaza denumirea firmei.",
                    parent=dialog,
                )
                return

            operator_id = self._slugify(
                display_name
            )

            if not operator_id:
                messagebox.showerror(
                    "ID invalid",
                    "Nu am putut genera ID-ul.",
                    parent=dialog,
                )
                return

            if (
                operator_id
                in self.operator_registry.operators
            ):
                messagebox.showerror(
                    "Operator existent",
                    f"Exista deja operatorul "
                    f"'{operator_id}'.",
                    parent=dialog,
                )
                return

            roles = (
                [
                    "food_responsible_operator",
                    "food_importer_eu",
                ]
                if target == "operator"
                else [
                    "supplier",
                    "distributor_ro",
                ]
            )

            self.operator_registry.operators[
                operator_id
            ] = {
                "display_name": display_name,
                "roles": roles,
                "address": {
                    "street": fields[
                        "street"
                    ].get().strip(),
                    "postal_code": fields[
                        "postal_code"
                    ].get().strip(),
                    "city": fields[
                        "city"
                    ].get().strip(),
                    "country": fields[
                        "country"
                    ].get().strip(),
                },
                "phone": "",
                "email": "",
                "notes": (
                    "Adaugat din interfata "
                    "K-Goodies Label Tool."
                ),
            }

            with self.operator_registry.registry_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    self.operator_registry.operators,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            self._refresh_operator_dropdowns()

            target_variable = (
                self.operator_var
                if target == "operator"
                else self.distributor_var
            )

            self._select_id(
                operator_id,
                target_variable,
            )

            dialog.destroy()

            self.status_var.set(
                f"Operator adaugat: {display_name}"
            )

        ttk.Button(
            frame,
            text="Salveaza operator",
            command=save_operator,
        ).grid(
            row=len(labels),
            column=1,
            pady=(18, 0),
            sticky="e",
        )

        frame.columnconfigure(
            1,
            weight=1,
        )

    @staticmethod
    def _slugify(value: str) -> str:
        value = value.lower().strip()

        replacements = {
            "ă": "a",
            "â": "a",
            "î": "i",
            "ș": "s",
            "ş": "s",
            "ț": "t",
            "ţ": "t",
        }

        for source, target in replacements.items():
            value = value.replace(
                source,
                target,
            )

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value,
        )

        return value.strip("-")


def main() -> None:
    root = Tk()
    LabelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()