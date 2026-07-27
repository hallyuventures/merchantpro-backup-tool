"""
MerchantPro Backup Tool

Main entry point.
"""
print("START")

from excel_reader import ExcelReader
from file_picker import select_excel_file
from downloader import Downloader
from validator import Validator
from product_serializer import ProductSerializer
from product_factory import ProductFactory

def banner():
    print("=" * 60)
    print(" MerchantPro Backup Tool")
    print("=" * 60)
    print()


def main():

    banner()

    print("Select the PRODUCTS export...\n")

    products = select_excel_file("Select MerchantPro Products Export")

    if products is None:
        print("Operation cancelled.")
        return

    print(products)
    print()

    print("Select the IMAGES export...\n")

    images = select_excel_file("Select MerchantPro Images Export")

    if images is None:
        print("Operation cancelled.")
        return

    print(images)
    print()

    reader = ExcelReader()

    reader.load_products(str(products))
    reader.load_images(str(images))
    image_map = reader.build_image_map()

    missing = Validator.find_products_without_images(
        reader.products,
        image_map,
    )

    print()
    print("=" * 60)
    print("VALIDATION")
    print("=" * 60)

    if not missing:
        print("All products have image records.")
    else:

        print(f"Products without image records: {len(missing)}")
        print()

    for product in missing:

        print(
            f'{product["id"]} - {product["name"]}'
        )

    print()
    downloader = Downloader()
    serializer = ProductSerializer()

    print()
    print("=" * 60)
    print("DOWNLOADING IMAGES")
    print("=" * 60)
    print()

    downloaded = 0

    for _, product_row in reader.products.iterrows():

        product_id = int(product_row["ID produs"])

        product_name = serializer.sanitize_filename(
            str(product_row["Nume produs"])
        )

        product_folder = (
            serializer.output /
            f"{product_id} - {product_name}"
        )

        product_folder.mkdir(exist_ok=True)

        images = image_map.get(product_id, [])

        # momentan doar verificăm că ProductFactory funcționează
        product = ProductFactory.from_excel(
            product_row,
            images
        )

        serializer.save(
            product_folder,
            product_row,
            images
        )

        for url in images:

            downloader.download(
                product_folder,
                url
            )

            downloaded += 1
            
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()

    print(f"Products with images : {len(image_map)}")
    print(f"Total image URLs     : {downloaded}")
    print()
    print("Done.")

    print(f"Products with images: {len(image_map)}")

    total = sum(len(v) for v in image_map.values())

    print(f"Total image URLs: {total}")

    print()

    first = next(iter(image_map))

    print("Example:")

    print(first)

    for url in image_map[first]:
        print("  ", url)


    print()
    print("Done.")


if __name__ == "__main__":
    main()