from src.product import Product
from src.label.engine import LabelEngine


product = Product(
    id=2,
    name=(
        "Frudia My Orchard Cherry Hand Cream, 30g"
    ),
    sku="TEST-BEAUTY-001",
    brand="Frudia",
    category="K-Beauty",
    price=0,
    country="Coreea de Sud",
    weight="30g",
    alcohol_content="",
    ingredients=(
        "Water, Glycerin, Butyrospermum Parkii Butter, "
        "Cetearyl Alcohol, Caprylic/Capric Triglyceride, "
        "Prunus Cerasus Fruit Extract, Fragrance."
    ),
    allergens="",
    nutrition="",
    preparation="",
    usage=(
        "Aplicati o cantitate potrivita pe maini si masati "
        "usor pana la absorbtia completa."
    ),
    expiry="A se vedea pe ambalaj.",
    extra_info=(
        "Doar pentru uz extern. Evitati contactul cu ochii. "
        "A nu se lasa la indemana copiilor."
    ),
    importer_distributor=(
        "Hallyu Ventures SRL, Romania"
    ),
)


LabelEngine().render(
    product,
    "label_beauty_test.png",
)