from date_helper import DateConverter
from datetime import datetime


def now():
    return datetime.now()


def test_should_be_of_this_year_and_month_when_convertion_with_ago():
    raw_dates = [
        "1 seconds ago",
        "1 hours ago",
        "1 minutes ago",
    ]
    for raw_date in raw_dates:
        converted_date = DateConverter.convert_news_raw_date(raw_date)
        assert converted_date.month == now().month
        assert converted_date.year == now().year


def test_convert_date_without_year_should_be_of_this_year():
    raw_date = "August 27"
    converted_date = DateConverter.convert_news_raw_date(raw_date)
    assert converted_date.year == now().year


def test_convert_full_date():
    raw_date = "August 27, 1856"
    expected = datetime.strptime(raw_date, "%B %d, %Y")
    assert DateConverter.convert_news_raw_date(raw_date) == expected
