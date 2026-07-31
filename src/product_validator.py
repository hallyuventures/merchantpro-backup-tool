from dataclasses import dataclass

from src.product import Product


@dataclass
class ValidationIssue:
    field: str
    message: str
    severity: str = "warning"


class ProductValidator:

    @staticmethod
    def validate(product: Product) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []

        ProductValidator._required(
            issues,
            product.name,
            "name",
            "Lipseste denumirea produsului",
            severity="error",
        )

        ProductValidator._required(
            issues,
            product.country,
            "country",
            "Lipseste tara de origine",
        )

        ProductValidator._required(
            issues,
            product.weight,
            "weight",
            "Lipseste greutatea sau volumul",
        )

        ProductValidator._required(
            issues,
            product.ingredients,
            "ingredients",
            "Lipseste campul Ingrediente/Alergeni",
        )

        ProductValidator._required(
            issues,
            product.expiry,
            "expiry",
            "Lipseste data expirarii",
        )

        if not product.supplier.strip():
            issues.append(
                ValidationIssue(
                    field="supplier",
                    message="Lipseste furnizorul intern din MerchantPro",
                )
            )

        category = product.category.lower()

        is_beauty = any(
            token in category
            for token in (
                "beauty",
                "cosmetic",
                "ingrijire",
                "health & care",
            )
        )

        is_food = any(
            token in category
            for token in (
                "food",
                "aliment",
                "snack",
                "ramen",
                "bauturi",
                "dulciuri",
            )
        )

        if is_beauty and not product.usage.strip():
            issues.append(
                ValidationIssue(
                    field="usage",
                    message="Lipseste modul de utilizare pentru produsul beauty",
                )
            )

        if is_food:
            ingredients_lower = product.ingredients.lower()

            if "alergen" not in ingredients_lower:
                issues.append(
                    ValidationIssue(
                        field="ingredients",
                        message=(
                            "Campul Ingrediente/Alergeni nu contine "
                            "o sectiune explicita pentru alergeni"
                        ),
                    )
                )

        if product.name.strip() and len(product.name.strip()) > 80:
            issues.append(
                ValidationIssue(
                    field="name",
                    message="Denumirea produsului este foarte lunga",
                )
            )

        if product.weight.strip() and len(product.weight.strip()) > 35:
            issues.append(
                ValidationIssue(
                    field="weight",
                    message="Campul Greutate/Volum este foarte lung",
                )
            )

        if (
            product.expiry.strip()
            and len(product.expiry.strip()) > 70
        ):
            issues.append(
                ValidationIssue(
                    field="expiry",
                    message="Campul Data expirare este foarte lung",
                )
            )

        return issues

    @staticmethod
    def _required(
        issues: list[ValidationIssue],
        value: str,
        field: str,
        message: str,
        severity: str = "info",
    ) -> None:
        if not value or not value.strip():
            issues.append(
                ValidationIssue(
                    field=field,
                    message=message,
                    severity=severity,
                )
            )