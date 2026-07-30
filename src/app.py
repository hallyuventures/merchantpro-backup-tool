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
from html_image_extractor import HtmlImageExtractor
from label_preview import LabelPreview
from pathlib import Path
from urllib.parse import urlparse

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
    preview = LabelPreview()

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

        product_images_folder = product_folder / "product_images"
        description_images_folder = product_folder / "description_images"

        product_images_folder.mkdir(exist_ok=True)
        description_images_folder.mkdir(exist_ok=True)
        
        product_images = image_map.get(product_id, [])

        description_images = HtmlImageExtractor.extract(
            str(product_row["Descriere produs"])
        )

        if description_images:

            print(
                f"Product {product_id}: "
                f"+{len(description_images)} image(s) from HTML"
            )

        # momentan doar verificăm că ProductFactory funcționează
        product = ProductFactory.from_excel(
            product_row,
            product_images,
            description_images
        )

        # preview.create(product)

        serializer.save(
            product_folder,
            product
        )

        for index, url in enumerate(product.images, start=1):

            extension = Path(urlparse(url).path).suffix.lower()

            if not extension:
                extension = ".jpg"

            filename = f"{index:03d}{extension}"

            downloader.download(
                product_images_folder,
                url,
                filename
            )

            downloaded += 1

        for index, url in enumerate(product.description_images, start=1):

            extension = Path(urlparse(url).path).suffix.lower()

            if not extension:
                extension = ".jpg"

            filename = f"{index:03d}{extension}"

            downloader.download(
                description_images_folder,
                url,
                filename
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