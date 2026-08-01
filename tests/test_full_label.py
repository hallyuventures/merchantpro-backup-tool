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
    name="Produs alimentar coreean test, 100g",
    sku="TEST-001",
    brand="Test Brand",
    category="K-Food",
    price=0,
    country="Coreea de Sud",
    weight="100g",
    alcohol_content="",
    ingredients=(
        "Faina de grau, zahar, ulei vegetal, amidon, sare, "
        "sirop de glucoza, arome si condimente."
    ),
    allergens="GRAU. Poate contine urme de LAPTE, SOIA si ARAHIDE.",
    nutrition=nutrition_html,
    preparation=(
        "Adaugati continutul intr-un vas cu 500 ml apa clocotita "
        "si fierbeti timp de 5 minute."
    ),
    usage="",
    expiry="A se vedea pe ambalaj.",
    extra_info=(
        "A se pastra intr-un loc uscat si racoros, ferit de "
        "lumina directa a soarelui."
    ),
    importer_distributor=(
        "Hallyu Ventures SRL, Romania"
    ),
)


LabelEngine().render(
    product,
    "label_full_test.png",
)