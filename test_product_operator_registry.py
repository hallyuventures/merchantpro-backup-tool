from src.operator_registry import OperatorRegistry
from src.product_operator_registry import (
    ProductOperatorRegistry,
)


operators = OperatorRegistry(
    "data/operators.json"
)

operators.load()

assignments = ProductOperatorRegistry(
    "data/product_operators.json"
)

assignments.load()

problems = assignments.validate(
    operators
)

print()
print("=" * 60)
print(" PRODUCT OPERATOR REGISTRY")
print("=" * 60)
print()

print(
    f"Asocieri incarcate: "
    f"{len(assignments.assignments)}"
)

if problems:
    print()
    print("Probleme:")

    for problem in problems:
        print(f"  - {problem}")
else:
    print("Toate asocierile sunt valide.")

print()

product_id = 424

responsible_id = (
    assignments.get_responsible_operator_id(
        product_id
    )
)

distributor_id = (
    assignments.get_distributor_id(
        product_id
    )
)

if responsible_id:
    print(
        operators.format_label(
            responsible_id,
            "Importator in UE",
        )
    )

if distributor_id:
    print()
    print(
        operators.format_label(
            distributor_id,
            "Distribuitor",
        )
    )