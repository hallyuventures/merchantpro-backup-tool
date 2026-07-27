from dataclasses import dataclass, field


@dataclass
class Product:

    id: int
    name: str
    sku: str

    brand: str
    category: str

    price: float

    country: str
    weight: str

    ingredients: str
    nutrition: str
    usage: str
    expiry: str
    extra_info: str

    images: list[str] = field(default_factory=list)