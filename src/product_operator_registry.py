import json
from pathlib import Path
from typing import Any


class ProductOperatorRegistryError(Exception):
    """Eroare legata de asocierea produselor cu operatorii."""


class ProductOperatorRegistry:

    def __init__(
        self,
        registry_path: str | Path = "data/product_operators.json",
    ):
        self.registry_path = Path(registry_path)
        self.assignments: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.assignments = {}
            self.save()
            return

        try:
            with self.registry_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ProductOperatorRegistryError(
                f"JSON invalid in {self.registry_path}: "
                f"linia {error.lineno}, coloana {error.colno}"
            ) from error

        if not isinstance(data, dict):
            raise ProductOperatorRegistryError(
                "Registrul trebuie sa fie un obiect JSON."
            )

        self.assignments = data

    def save(self) -> None:
        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.registry_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.assignments,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def get(
        self,
        product_id: int | str,
    ) -> dict[str, Any] | None:
        return self.assignments.get(
            str(product_id)
        )

    def get_responsible_operator_id(
        self,
        product_id: int | str,
    ) -> str:
        assignment = self.get(product_id)

        if not assignment:
            return ""

        return str(
            assignment.get(
                "responsible_operator_id",
                "",
            )
        ).strip()

    def get_distributor_id(
        self,
        product_id: int | str,
    ) -> str:
        assignment = self.get(product_id)

        if not assignment:
            return ""

        return str(
            assignment.get(
                "distributor_id",
                "",
            )
        ).strip()

    def set_assignment(
        self,
        product_id: int | str,
        responsible_operator_id: str,
        distributor_id: str = "",
    ) -> None:
        product_key = str(product_id)

        self.assignments[product_key] = {
            "responsible_operator_id": (
                responsible_operator_id.strip()
            ),
            "distributor_id": distributor_id.strip(),
        }

        self.save()

    def remove_assignment(
        self,
        product_id: int | str,
    ) -> None:
        self.assignments.pop(
            str(product_id),
            None,
        )

        self.save()

    def validate(
        self,
        operator_registry,
    ) -> list[str]:
        problems: list[str] = []

        for product_id, assignment in self.assignments.items():
            if not isinstance(assignment, dict):
                problems.append(
                    f"Produs {product_id}: "
                    "asocierea nu este obiect"
                )
                continue

            responsible_id = str(
                assignment.get(
                    "responsible_operator_id",
                    "",
                )
            ).strip()

            distributor_id = str(
                assignment.get(
                    "distributor_id",
                    "",
                )
            ).strip()

            if (
                responsible_id
                and operator_registry.get(
                    responsible_id
                ) is None
            ):
                problems.append(
                    f"Produs {product_id}: "
                    f"operator necunoscut '{responsible_id}'"
                )

            if (
                distributor_id
                and operator_registry.get(
                    distributor_id
                ) is None
            ):
                problems.append(
                    f"Produs {product_id}: "
                    f"distribuitor necunoscut "
                    f"'{distributor_id}'"
                )

        return problems