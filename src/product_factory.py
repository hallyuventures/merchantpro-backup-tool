from product import Product


class ProductFactory:

    @staticmethod
    def from_excel(
        row,
        product_images,
        description_images
        ):

        return Product(

            id=int(row["ID produs"]),

            name=str(row["Nume produs"]),

            sku=str(row["Cod produs - SKU"]),

            brand=str(row["Producator"]),

            category=str(row["Categorie principala"]),

            price=float(row["Pret produs"]),

            country=str(row["Produs in"]),

            weight=str(row["Greutate/Volum"]),

            ingredients=str(row["Ingrediente/Alergeni"]),

            allergens=str(row["Alergeni"]),

            nutrition=str(row["Valori nutritionale"]),

            preparation=str(row["Mod de preparare"]),
            
            usage=str(row["Mod utilizare"]),

            expiry=str(row["Data expirare"]),

            extra_info=str(row["Informatii suplimentare"]),

            importer_distribuitor="",
            
            images=product_images,

            description_images=description_images,

            description_html=str(
                row["Descriere produs"]
            ),
        )