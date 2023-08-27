from datetime import datetime
from datetime import date
import re
import uuid
from dateutil.relativedelta import relativedelta


class News:
    def __init__(
        self,
        title: str,
        description: str,
        date: str,
        image_url: str,
    ):
        self._title = title
        self._description = description
        self._date = self._convert_date(date)
        self._image_url = image_url

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def date(self) -> date:
        return self._date

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def image_name(self) -> str:
        return f"{uuid.uuid4()}.jpeg"

    def count_search_phrase(self, search_phrase: str) -> int:
        return (
            self.description.lower().count(search_phrase.lower())
            + self.title.lower().count(search_phrase.lower())
        )

    @property
    def contains_any_amount_of_money(self) -> bool:
        money_patterns = [
            r'\$\d+\.\d+',  # $11.1 | $111,111.11
            r'\d+\s*dollars',  # 11 dollars
            r'\d+\s*USD'  # 11 USD
        ]
        return any((
            re.search(pattern, self.title)
            or re.search(pattern, self.description)
            for pattern in money_patterns
        ))

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat(),
            "image_name": self.image_name,
            "contains_amount_of_money": self.contains_any_amount_of_money,
        }

    def _convert_date(self, article_date: str) -> date:
        if 'hours ago' in article_date:
            current_date = datetime.now()
            hours = int(article_date.split(' ')[0])
            date_converted = current_date - relativedelta(hours=hours)

        elif 'minutes ago' in article_date:
            current_date = datetime.now()
            minutes = int(article_date.split(' ')[0])
            date_converted = current_date - relativedelta(minutes=minutes)

        elif 'seconds ago' in article_date:
            current_date = datetime.now()
            seconds = int(article_date.split(' ')[0])
            date_converted = current_date - relativedelta(seconds=seconds)

        elif len(article_date.split(',')) == 2:
            date_converted = datetime.strptime(article_date, "%B %d, %Y")

        else:
            date_converted = datetime.strptime(f'{article_date}, {datetime.now().year}', "%B %d, %Y")

        return date_converted
