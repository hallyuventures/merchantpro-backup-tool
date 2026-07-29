from src.product import Product
from src.label.engine import LabelEngine


nutrition_html = """
<div>
    Valori nutritionale tipice
    per 100g | per portie (5g)
</div>
<div>
    Valoare energetica
    2494kJ / 610kcal | 125kJ / 30kcal
</div>
<div>Grasimi 47,9g | 2,4g</div>
<div>
    din care acizi grasi saturati
    4,8g | 0,2g
</div>
<div>Glucide 24,3g | 1,2g</div>
<div>din care zaharuri 0,7g | 0g</div>
<div>Proteine 19,4g | 1,0g</div>
<div>Sare 2,9g | 0,1g</div>
"""


product = Product(
    id=1,
    name="Produs alimentar test, 100g",
    sku="",
    brand="",
    category="K-Food",
    price=0,
    country="Coreea de Sud",
    weight="100g",
    ingredients="Apa, faina, zahar, sare",
    allergens="GRAU",
    nutrition=nutrition_html,
    preparation="",  
    usage="",
    expiry="A se vedea pe ambalaj.",
    extra_info="",
)


LabelEngine().render(
    product,
    "label_nutrition.png",
)