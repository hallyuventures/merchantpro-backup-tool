"""
MerchantPro Backup Tool

Main entry point.
"""

from excel_reader import ExcelReader
from file_picker import select_excel_file
from downloader import Downloader
from validator import Validator

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

    print()
    print("=" * 60)
    print("DOWNLOADING IMAGES")
    print("=" * 60)
    print()

    downloaded = 0

    for product_id, urls in image_map.items():

        print(f"Product {product_id}: {len(urls)} image(s)")

        for url in urls:

            downloader.download(product_id, url)
            downloaded += 1

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Products with images : {len(image_map)}")
    print(f"Total image URLs     : {downloaded}")
    print()
    print("Done.")

    print()
    print("Downloading first image...")
    print()

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