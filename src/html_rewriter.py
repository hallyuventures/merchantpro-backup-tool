from html_image_extractor import HtmlImageExtractor


class HtmlRewriter:

    @staticmethod
    def rewrite(html: str) -> str:

        images = HtmlImageExtractor.extract(html)

        for index, url in enumerate(images, start=1):

            extension = ".jpg"

            if "." in url.split("/")[-1]:
                extension = "." + url.split("/")[-1].split(".")[-1].split("?")[0]

            filename = f"description_images/{index:03d}{extension}"

            html = html.replace(url, filename)

        return html