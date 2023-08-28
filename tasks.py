from date_helper import DateConverter
from download_pictures import PictureDownloader
from exceptions import InvalidInput
from homepage_handler import HomePageHandler
from search_page_handler import SearchPageHandler
from RPA.Browser.Selenium import Selenium

from robocorp.tasks import task
from robocorp import workitems, log
from excel_report import ExcelReport

browser_lib = Selenium()


def validate_inputs(**inputs):
    if not inputs.get("searchPhrase"):
        raise InvalidInput("searchPhrase is required")
    if inputs.get("numberOfMonths") < 0:
        raise InvalidInput("numberOfMonths must be greater than or equal to 0")


@task
def extract_nyt_news():
    try:
        work_items = workitems.inputs.current.payload
        SEARCH_PHRASE = work_items.get("searchPhrase")
        CATEGORIES = work_items.get("categories", [])
        NUMBER_OF_MONTHS = work_items.get("numberOfMonths", 0)
        validate_inputs(searchPhrase=SEARCH_PHRASE,
                        numberOfMonths=NUMBER_OF_MONTHS)

        HomePageHandler(browser_lib).search(SEARCH_PHRASE)

        search_page_handler = SearchPageHandler(browser_lib)
        search_page_handler.accept_cookies()
        search_page_handler.sort_by_newest()
        search_page_handler.select_categories(CATEGORIES)

        end_date = DateConverter.get_end_date_from_months(NUMBER_OF_MONTHS)
        news = search_page_handler.get_news_until(end_date)

        PictureDownloader.download(news)
        ExcelReport.generate(news, SEARCH_PHRASE)

        browser_lib.close_all_browsers()

    except InvalidInput as e:
        raise e

    except Exception as e:
        raise e
