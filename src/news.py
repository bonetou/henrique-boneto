from datetime import datetime
import re
import uuid
from src.date_helper import DateConverter


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
    def converted_date(self) -> datetime:
        return self._date

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def image_name(self) -> str:
        return f"{uuid.uuid4()}.jpeg" if self.image_url else ""

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "date": self.converted_date.isoformat(),
            "image_name": self.image_name,
            "image_url": self.image_url,
        }
