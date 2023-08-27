import time
from RPA.Browser.Selenium import Selenium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from robocorp.tasks import task
from robocorp import log, workitems
from RPA.Excel.Files import Files
import requests
from RPA.FileSystem import FileSystem

browser_lib = Selenium()

def open_website(url):
    browser_lib.open_available_browser(url)
    browser_lib.wait_until_page_contains_element("//div[@id='complianceOverlay']")
    browser_lib.click_button('Continue')

def search_for(search_phrase: str):
    browser_lib.click_button('SEARCH')
    browser_lib.input_text('//*[@id="search-input"]/form/div/input', search_phrase)
    browser_lib.click_button('Go')

def sort_by_newest():
    browser_lib.select_from_list_by_value('//*[@id="site-content"]/div[1]/div[1]/div[1]/form/div[2]/div/select', 'newest')

def select_categories(categories: list):
    browser_lib.click_button("//button[@data-testid='search-multiselect-button']")
    for category in categories:
        category_checkbox = browser_lib.find_element(f'//input[@type="checkbox" and contains(@value, "{category}")]')
        if not category_checkbox.is_selected():
            category_checkbox.click()

def get_end_date(number_of_months: int):
    current_date = datetime.now().date()
    if number_of_months == 0:
        end_date = current_date - relativedelta(months=number_of_months)
    else:
        end_date = current_date - relativedelta(months=number_of_months-1)
    return end_date

def get_news_data():
    news_data = []
    all_news = browser_lib.find_elements("//li[@data-testid='search-bodega-result']")
    for news in all_news:

        title = browser_lib.find_element("css:h4", news).text
        log.info(title)
        try:
            description = browser_lib.find_element("css:a", news).text
        except:
            description = ''
        log.info(description)
        date = browser_lib.find_element("css:span", news).get_attribute('aria-label')
        log.info(date)
        if 'hours ago' in date:
            current_date = datetime.now()
            hours = int(date.split(' ')[0])
            date_converted = current_date - relativedelta(hours=hours)
        elif 'minutes ago' in date:
            current_date = datetime.now()
            minutes = int(date.split(' ')[0])
            date_converted = current_date - relativedelta(minutes=minutes)
        elif 'seconds ago' in date:
            current_date = datetime.now()
            seconds = int(date.split(' ')[0])
            date_converted = current_date - relativedelta(seconds=seconds)
        elif len(date.split(',')) == 2:
            date_converted = datetime.strptime(date, "%B %d, %Y")
        else:
            date_converted = datetime.strptime(f'{date}, {datetime.now().year}', "%B %d, %Y")
        try:
            image_url = browser_lib.find_element("css:img", news).get_attribute('src')
        except:
            image_url = ''
        log.info(image_url)
        news_data.append({
            'title': title,
            'description': description,
            'date': date_converted,
            'image_url': image_url
        })
    return news_data

def filter_news_by_date(news_data: list, end_date: datetime):
    filtered_news = []
    for news in news_data:
        if (news['date'].month, news['date'].year) >= (end_date.month, end_date.year):
            filtered_news.append(news)
    return filtered_news

def exists_show_more_button():
    return browser_lib.is_element_visible("//button[@data-testid='search-show-more-button']")


@task
def minimal_task():
    item = workitems.inputs.current.payload
    SEARCH_PHRASE = item.get("searchPhrase", "turtle")
    CATEGORIES = item.get("categories", [])
    NUMBER_OF_MONTHS = item.get("numberOfMonths", 0)
    open_website(url="https://www.nytimes.com/")
    all_news = []
    search_for(SEARCH_PHRASE)
    sort_by_newest()
    select_categories(CATEGORIES)
    browser_lib.click_button_when_visible('//button[@data-testid="GDPR-accept"]')
    end_date = get_end_date(NUMBER_OF_MONTHS)

    while True:
        all_news_from_search_page = get_news_data()
        time.sleep(2)
        all_news_in_selected_months = filter_news_by_date(all_news_from_search_page, end_date)
        all_news = all_news_in_selected_months.copy()

        if len(all_news_in_selected_months) != len(all_news_from_search_page):
            break
    
        if not exists_show_more_button():
            break
        
        browser_lib.click_button_when_visible("//button[@data-testid='search-show-more-button']")

    file_system = FileSystem()
    file_system.create_directory("output/article_images")
    for news in all_news:
        if news['image_url']:
            response = requests.get(news['image_url'])
            if response.status_code == 200:
                with open(f"output/article_images/{news['title']}.jpg", "wb") as f:
                    f.write(response.content)

    excel_lib = Files()
    excel_lib.create_workbook("output/articles.xlsx")
    excel_lib.create_worksheet(name="articles", content=all_news, header=True)
    excel_lib.save_workbook()
