from datetime import datetime
import re
import uuid
from date_helper import DateConverter


class News:
    def __init__(
        self,
        title: str,
        description: str,
        raw_date: str,
        image_url: str,
    ):
        self._title = title
        self._description = description
        self._date = DateConverter.convert_news_raw_date(raw_date)
        self._image_url = image_url

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def news_date(self) -> datetime:
        return self._date

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def image_name(self) -> str:
        return f"{uuid.uuid4()}.jpeg" if self.image_url else ""

    @property
    def contains_any_amount_of_money(self) -> bool:
        possible_money_patterns = [
            r'\$\d+(\.\d+)?',      # $11.1 | $111,111.11
            r'\d+\s*dollars',   # 11 dollars
            r'\d+\s*USD'        # 11 USD
        ]
        return any((
            re.search(pattern, self.title)
            or re.search(pattern, self.description)
            for pattern in possible_money_patterns
        ))

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "date": self.news_date.isoformat(),
            "image_name": self.image_name,
            "contains_amount_of_money": self.contains_any_amount_of_money,
        }
