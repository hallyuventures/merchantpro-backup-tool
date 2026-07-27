import re


class HtmlImageExtractor:

    @staticmethod
    def extract(html: str) -> list[str]:

        if not html:
            return []

        pattern = r'<img[^>]+src="([^"]+)"'

        return re.findall(pattern, html)