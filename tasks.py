from nyt_homepage_handler import NYTHomePageHandler
from nyt_search_page_handler import NYTSearchPageHandler
from RPA.Browser.Selenium import Selenium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from robocorp.tasks import task
from robocorp import log, workitems
from RPA.Excel.Files import Files
import requests
from uuid import uuid4

browser_lib = Selenium()


def get_end_date(number_of_months: int):
    current_date = datetime.now().date()
    if number_of_months == 0:
        end_date = current_date - relativedelta(months=number_of_months)
    else:
        end_date = current_date - relativedelta(months=number_of_months-1)
    return end_date


@task
def extract_nyt_articles():
    work_items = workitems.inputs.current.payload
    SEARCH_PHRASE = work_items.get("searchPhrase", "turtle")
    CATEGORIES = work_items.get("categories", [])
    NUMBER_OF_MONTHS = work_items.get("numberOfMonths", 0)
    end_date = get_end_date(NUMBER_OF_MONTHS)

    home_page_handler = NYTHomePageHandler(browser_lib)
    search_page_handler = NYTSearchPageHandler(browser_lib)

    home_page_handler.search(SEARCH_PHRASE)
    search_page_handler.sort_by_newest()
    search_page_handler.select_categories(CATEGORIES)
    search_page_handler.accept_cookies()
    articles = search_page_handler.get_articles_until(end_date)
    generate_excel_file(articles)


def generate_excel_file(all_news: list):
    for news in all_news:
        if news['image_url']:
            response = requests.get(news['image_url'])
            if response.status_code == 200:
                with open(f"output/{uuid4()}.jpg", "wb") as f:
                    f.write(response.content)

    excel_lib = Files()
    excel_lib.create_workbook("output/articles.xlsx")
    excel_lib.create_worksheet(name="articles", content=all_news, header=True)
    excel_lib.save_workbook()
