from datetime import date
import re


class ArticleData:
    def __init__(
        self,
        title: str,
        description: str,
        date: date,
        image_url: str,
    ):
        self._title = title
        self._description = description
        self._date = date
        self._image_url = image_url

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def date(self):
        return self._date

    @property
    def image_url(self):
        return self._image_url

    def count_search_phrase(self, search_phrase: str) -> int:
        return (
            self._article_data.description.lower().count(search_phrase.lower())
            + self._article_data.title.lower().count(search_phrase.lower())
        )

    def is_any_amount_of_money(self) -> bool:
        patterns = [
            r'\$\d+\.\d+',
            r'\d+\s*dollars',
            r'\d+\s*USD'
        ]
        return any((
            re.search(pattern, self._article_data.description)
            or re.search(pattern, self._article_data.title)
            for pattern in patterns
        ))
