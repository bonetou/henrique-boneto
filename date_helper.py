from datetime import datetime
from dateutil.relativedelta import relativedelta


class DateConverter:
    _date_format = "%B %d, %Y"

    @classmethod
    def _current_date(cls):
        return datetime.now()

    @classmethod
    def convert_news_raw_date(cls, raw_date: str) -> datetime:
        # Example: 2 hours ago
        if 'hours ago' in raw_date:
            hours = raw_date.split(' ')[0]
            return cls._convert_relative(hours, 'hours')

        # Example: 2 minutes ago
        elif 'minutes ago' in raw_date:
            minutes = raw_date.split(' ')[0]
            return cls._convert_relative(minutes, 'minutes')

        # Example: 2 seconds ago
        elif 'seconds ago' in raw_date:
            seconds = raw_date.split(' ')[0]
            return cls._convert_relative(seconds, 'seconds')

        # Example: August 27
        elif len(raw_date.split(',')) == 2:
            return datetime.strptime(raw_date, cls._date_format)

        # Example: August 27, 1856
        return datetime.strptime(f'{raw_date}, {cls._current_date().year}',
                                 cls._date_format)

    @classmethod
    def get_end_date_from_months(cls, number_of_months: int) -> datetime:
        delta_months = 0 if number_of_months == 0 else number_of_months - 1
        return cls._current_date().date() - relativedelta(months=delta_months)

    @classmethod
    def _convert_relative(cls, value: str, unit: str) -> datetime:
        return cls._current_date() - relativedelta(**{unit: int(value)})
