from src.label.nutrition_parser import NutritionParser


html = """
<div>
    <strong>
        Valori nutritionale tipice per 100g | per portie (5g)
    </strong>
</div>

<div>
    <strong>Valoare energetica</strong>
    2494kJ / 610kcal | 125kJ / 30kcal
</div>

<div>
    <strong>Grasimi</strong>
    47,9g | 2,4g
</div>

<div>
    din care acizi grasi saturati
    4,8g | 0,2g
</div>

<div>
    Glucide
    24,3g | 1,2g
</div>

<div>
    din care zaharuri
    0,7g | 0g
</div>

<div>
    Proteine
    19,4g | 1,0g
</div>

<div>
    Sare
    2,9g | 0,1g
</div>
"""


nutrition = NutritionParser.parse(html)

print("HEADERS:")
print(nutrition.headers)

print("\nROWS:")

for row in nutrition.rows:
    print(f"{row.label} => {row.values}")

print("\nEMPTY:")
print(nutrition.is_empty)