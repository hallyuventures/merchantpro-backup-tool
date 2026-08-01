from src.operator_registry import OperatorRegistry


registry = OperatorRegistry(
    "data/operators.json"
)

registry.load()

problems = registry.validate()

print()
print("=" * 60)
print(" OPERATOR REGISTRY")
print("=" * 60)
print()

print(
    f"Operatori incarcati: "
    f"{len(registry.operators)}"
)

if problems:
    print()
    print("Probleme:")

    for problem in problems:
        print(f"  - {problem}")
else:
    print("Structura registrului este valida.")

print()
print(
    registry.format_label(
        "panasia-handels-gmbh",
        "Importator in UE",
    )
)