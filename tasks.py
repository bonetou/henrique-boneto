from download_pictures import PictureDownloader
from homepage_handler import HomePageHandler
from search_page_handler import SearchPageHandler
from RPA.Browser.Selenium import Selenium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from robocorp.tasks import task
from robocorp import workitems
from RPA.Excel.Files import Files
import requests
from uuid import uuid4
from excel_report import ExcelReport
browser_lib = Selenium()


@task
def extract_nyt_articles():
    work_items = workitems.inputs.current.payload
    SEARCH_PHRASE = work_items.get("searchPhrase", "turtle")
    CATEGORIES = work_items.get("categories", [])
    NUMBER_OF_MONTHS = work_items.get("numberOfMonths", 0)
    end_date = get_end_date(NUMBER_OF_MONTHS)

    HomePageHandler(browser_lib).search(SEARCH_PHRASE)

    search_page_handler = SearchPageHandler(browser_lib)
    search_page_handler.accept_cookies()
    search_page_handler.sort_by_newest()
    search_page_handler.select_categories(CATEGORIES)
    news = search_page_handler.get_news_until(end_date)
    PictureDownloader.download(news)
    ExcelReport.generate(news, SEARCH_PHRASE)


def get_end_date(number_of_months: int):
    current_date = datetime.now().date()
    if number_of_months == 0:
        end_date = current_date - relativedelta(months=number_of_months)
    else:
        end_date = current_date - relativedelta(months=number_of_months-1)
    return end_date
