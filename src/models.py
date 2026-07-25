"""
MerchantPro Backup Tool
models.py

Data models used by the application.
"""

from dataclasses import dataclass, field


@dataclass
class ProductImage:
    image_id: int
    url: str
    filename: str = ""


@dataclass
class Product:
    product_id: int
    name: str = ""
    images: list[ProductImage] = field(default_factory=list)

    def add_image(self, image: ProductImage):
        self.images.append(image)