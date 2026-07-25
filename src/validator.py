"""
MerchantPro Backup Tool
Validator
"""


class Validator:

    @staticmethod
    def find_products_without_images(products_df, image_map):

        missing = []

        for _, row in products_df.iterrows():

            product_id = int(row["ID produs"])

            if product_id not in image_map:

                missing.append(
                    {
                        "id": product_id,
                        "name": row["Nume produs"],
                    }
                )

        return missing