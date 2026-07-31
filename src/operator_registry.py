import json
from pathlib import Path
from typing import Any


class OperatorRegistryError(Exception):
    """Eroare legata de registrul operatorilor."""


class OperatorRegistry:

    REQUIRED_ADDRESS_FIELDS = (
        "street",
        "postal_code",
        "city",
        "country",
    )

    def __init__(
        self,
        registry_path: str | Path = "data/operators.json",
    ):
        self.registry_path = Path(registry_path)
        self.operators: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        if not self.registry_path.exists():
            raise FileNotFoundError(
                f"Registrul operatorilor nu exista: "
                f"{self.registry_path}"
            )

        try:
            with self.registry_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise OperatorRegistryError(
                f"JSON invalid in {self.registry_path}: "
                f"linia {error.lineno}, coloana {error.colno}"
            ) from error

        if not isinstance(data, dict):
            raise OperatorRegistryError(
                "Registrul operatorilor trebuie sa fie un obiect JSON."
            )

        self.operators = data

    def get(
        self,
        operator_id: str,
    ) -> dict[str, Any] | None:
        return self.operators.get(operator_id)

    def require(
        self,
        operator_id: str,
    ) -> dict[str, Any]:
        operator = self.get(operator_id)

        if operator is None:
            raise OperatorRegistryError(
                f"Operator necunoscut: {operator_id}"
            )

        return operator

    def find_by_role(
        self,
        role: str,
    ) -> list[tuple[str, dict[str, Any]]]:
        matches = []

        for operator_id, operator in self.operators.items():
            roles = operator.get("roles", [])

            if role in roles:
                matches.append(
                    (
                        operator_id,
                        operator,
                    )
                )

        return matches

    def validate(self) -> list[str]:
        problems: list[str] = []

        for operator_id, operator in self.operators.items():
            display_name = str(
                operator.get("display_name", "")
            ).strip()

            if not display_name:
                problems.append(
                    f"{operator_id}: lipseste display_name"
                )

            roles = operator.get("roles", [])

            if not isinstance(roles, list) or not roles:
                problems.append(
                    f"{operator_id}: lipsesc roles"
                )

            address = operator.get("address", {})

            if not isinstance(address, dict):
                problems.append(
                    f"{operator_id}: address nu este obiect"
                )
                continue

            for field in self.REQUIRED_ADDRESS_FIELDS:
                if field not in address:
                    problems.append(
                        f"{operator_id}: lipseste address.{field}"
                    )

        return problems

    def format_address(
        self,
        operator_id: str,
    ) -> str:
        operator = self.require(operator_id)
        address = operator.get("address", {})

        street = str(
            address.get("street", "")
        ).strip()

        postal_code = str(
            address.get("postal_code", "")
        ).strip()

        city = str(
            address.get("city", "")
        ).strip()

        country = str(
            address.get("country", "")
        ).strip()

        locality_parts = [
            value
            for value in (
                postal_code,
                city,
            )
            if value
        ]

        locality = " ".join(locality_parts)

        address_parts = [
            value
            for value in (
                street,
                locality,
                country,
            )
            if value
        ]

        return ", ".join(address_parts)

    def format_label(
        self,
        operator_id: str,
        role_label: str,
    ) -> str:
        operator = self.require(operator_id)

        display_name = str(
            operator.get("display_name", "")
        ).strip()

        address = self.format_address(
            operator_id
        )

        lines = [
            f"{role_label}:",
            display_name,
        ]

        if address:
            lines.append(address)

        return "\n".join(lines)