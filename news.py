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
        self._date = self.convert_date(date)
        self._image_url = image_url

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def news_date(self) -> date:
        return self._date

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def image_name(self) -> str:
        return f"{uuid.uuid4()}.jpeg" if self.image_url else ""

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
            "date": self.news_date.isoformat(),
            "image_name": self.image_name,
            "contains_amount_of_money": self.contains_any_amount_of_money,
        }

    @classmethod
    def convert_date(cls, news_date: str) -> date:
        if 'hours ago' in news_date:
            current_date = datetime.now()
            hours = int(news_date.split(' ')[0])
            date_converted = current_date - relativedelta(hours=hours)

        elif 'minutes ago' in news_date:
            current_date = datetime.now()
            minutes = int(news_date.split(' ')[0])
            date_converted = current_date - relativedelta(minutes=minutes)

        elif 'seconds ago' in news_date:
            current_date = datetime.now()
            seconds = int(news_date.split(' ')[0])
            date_converted = current_date - relativedelta(seconds=seconds)

        elif len(news_date.split(',')) == 2:
            date_converted = datetime.strptime(news_date, "%B %d, %Y")

        else:
            date_converted = datetime.strptime(f'{news_date}, {datetime.now().year}', "%B %d, %Y")

        return date_converted
