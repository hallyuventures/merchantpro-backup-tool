"""
MerchantPro Backup Tool
Excel reader
"""

from pathlib import Path
import pandas as pd


class ExcelReader:

    def __init__(self):
        self.products = None
        self.images = None

    def load_products(self, filename: str):

        print(f"Loading products: {Path(filename).name}")

        self.products = pd.read_excel(filename)

        print(f"Products: {len(self.products)}")
        print()

    def load_images(self, filename: str):

        print(f"Loading images: {Path(filename).name}")

        self.images = pd.read_excel(filename)

        print(f"Images: {len(self.images)}")
        print()

    def build_image_map(self):

        image_map = {}

        for _, row in self.images.iterrows():

            product_id = int(row["ID produs"])
            url = str(row["URL imagine"]).strip()

            image_map.setdefault(product_id, []).append(url)

        return image_map