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

            country=str(
                row.get("Produs in", "")
            ),

            weight=str(
                row.get("Greutate/Volum", "")
            ),
            
            alcohol_content=str(
                row.get("Continut alcool", "")
            ),

            ingredients=str(
                row.get("Ingrediente/Alergeni", "")
            ),

            allergens="",

            nutrition=str(
                row.get("Valori nutritionale", "")
            ),

            preparation=str(
                row.get("Mod preparare", "")
            ),
            
            usage=str(
                row.get("Mod utilizare", "")
            ),

            expiry=str(
                row.get("Data expirare", "")
            ),

            extra_info=str(
                row.get("Informatii suplimentare", "")
            ),

            importer_distributor=str(
                row.get("Importator/Distribuitor", "")
            ),
            
            images=product_images,

            description_images=description_images,

            description_html=str(
                row["Descriere produs"]
            ),
        )