import re


def html_to_text(html: str) -> str:

    if not html:
        return ""

    text = re.sub(r"<[^>]+>", "", str(html))

    text = text.replace("&nbsp;", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()