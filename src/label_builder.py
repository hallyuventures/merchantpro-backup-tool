from product import Product


class LabelBuilder:

    def build(
            self,
            product: Product
    ):


        print()

        print("=" * 60)
        print("LABEL BUILDER")
        print("=" * 60)

        print(product.name)
        print(product.price)
        print(product.id)

        return Label(
            title=product.name,
            price=product.price,
            barcode=product.sku
        )