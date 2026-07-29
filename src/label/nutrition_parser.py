from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
import re


@dataclass
class NutritionRow:
    label: str
    values: list[str] = field(default_factory=list)


@dataclass
class NutritionData:
    headers: list[str] = field(default_factory=list)
    rows: list[NutritionRow] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.rows


class _NutritionHTMLParser(HTMLParser):

    BLOCK_TAGS = {
        "div",
        "p",
        "br",
        "li",
        "tr",
    }

    def __init__(self):
        super().__init__()

        self.lines: list[str] = []
        self.current_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "br":
            self._flush_line()

    def handle_endtag(self, tag):
        if tag.lower() in self.BLOCK_TAGS:
            self._flush_line()

    def handle_data(self, data):
        text = unescape(data)

        if text.strip():
            self.current_parts.append(text)

    def _flush_line(self):
        text = " ".join(self.current_parts)
        text = NutritionParser.normalize_spaces(text)

        if text:
            self.lines.append(text)

        self.current_parts = []

    def close(self):
        self._flush_line()
        super().close()


class NutritionParser:

    TITLE_PATTERN = re.compile(
        r"^valori(?:\s+nutritionale)?\s+tipice\s*",
        re.IGNORECASE,
    )

    KNOWN_LABELS = (
        "valoare energetica",
        "din care acizi grasi saturati",
        "acizi grasi saturati",
        "din care grasimi saturate",
        "din care saturate",
        "grasimi",
        "carbohidrati",
        "din care zaharuri",
        "zaharuri",
        "glucide",
        "fibre",
        "proteine",
        "sare",
    )

    @classmethod
    def parse(cls, html: str | None) -> NutritionData:
        if not html or not html.strip():
            return NutritionData()

        parser = _NutritionHTMLParser()
        parser.feed(html)
        parser.close()

        lines = cls._clean_lines(parser.lines)

        if not lines:
            return NutritionData()

        headers: list[str] = []
        rows: list[NutritionRow] = []

        if cls._is_title(lines[0]):
            headers = cls._parse_headers(lines[0])
            lines = lines[1:]

        for line in lines:
            row = cls._parse_row(line)

            if row is not None:
                rows.append(row)

        return NutritionData(
            headers=headers,
            rows=rows,
        )

    @staticmethod
    def normalize_spaces(text: str) -> str:
        text = unescape(text)
        text = text.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @classmethod
    def _clean_lines(cls, lines: list[str]) -> list[str]:
        cleaned: list[str] = []

        for line in lines:
            line = cls.normalize_spaces(line)

            if line:
                cleaned.append(line)

        return cleaned

    @classmethod
    def _is_title(cls, line: str) -> bool:
        return bool(cls.TITLE_PATTERN.match(line))

    @classmethod
    def _parse_headers(cls, line: str) -> list[str]:
        header_text = cls.TITLE_PATTERN.sub("", line)
        header_text = header_text.strip(" :-")

        if not header_text:
            return []

        parts = re.split(r"\s*\|\s*", header_text)

        return [
            cls.normalize_spaces(part)
            for part in parts
            if cls.normalize_spaces(part)
        ]

    @classmethod
    def _parse_row(
        cls,
        line: str,
    ) -> NutritionRow | None:
        normalized = cls.normalize_spaces(line)

        label = cls._extract_label(normalized)

        if label is None:
            return None

        remainder = normalized[len(label):]
        remainder = remainder.strip(" :-")

        values = [
            cls.normalize_spaces(value)
            for value in re.split(r"\s*\|\s*", remainder)
        ]

        values = [
            value
            for value in values
            if value
        ]

        return NutritionRow(
            label=label,
            values=values,
        )

    @classmethod
    def _extract_label(
        cls,
        line: str,
    ) -> str | None:
        lowered = line.lower()

        for known_label in sorted(
            cls.KNOWN_LABELS,
            key=len,
            reverse=True,
        ):
            if lowered.startswith(known_label):
                return line[:len(known_label)].strip()

        return None