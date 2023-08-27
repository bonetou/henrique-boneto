from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import ElementNotFound
from selenium.webdriver.remote.webelement import WebElement
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class NYTSearchPageHandler:
    _SORT_BY_SELECT_LOCATOR = '//*[@id="site-content"]/div[1]/div[1]/div[1]/form/div[2]/div/select'  # noqa
    _CATEGORIES_BUTTON_LOCATOR = "//button[@data-testid='search-multiselect-button']"  # noqa
    _COOKIES_BUTTON_LOCATOR = '//button[@data-testid="GDPR-accept"]'
    _SEARCH_RESULTS_LOCATOR = "//li[@data-testid='search-bodega-result']"
    _ARTICLE_TITLE_LOCATOR = "css:h4"
    _ARTICLE_DESCRIPTION_LOCATOR = "css:a"
    _SHOW_MORE_BUTTON_LOCATOR = "//button[@data-testid='search-show-more-button']"  # noqa

    def __init__(self, browser: Selenium):
        self.browser = browser

    def get_articles_until(self, end_date: date):
        while (
            self.exists_show_more_button
            and not self._has_articles_reached_end_date(self.get_articles(), end_date)
        ):
            self._click_show_more_button()
        return self._filter_articles_by_end_date(self.get_articles(), end_date)

    def get_articles(self):
        news_data = []
        article_results = self.browser.find_elements(
            self._SEARCH_RESULTS_LOCATOR
        )

        for article in article_results:
            news_data.append({
                'title': self._get_article_title(article),
                'description': self._get_article_description(article),
                'date': self._get_date(article),
                'image_url': self._get_image_url(article)
            })
        return news_data

    def sort_by_newest(self):
        self.browser.select_from_list_by_value(
            self._SORT_BY_SELECT_LOCATOR,
            'newest',
        )

    def select_categories(self, categories: list):
        self.browser.click_button(self._CATEGORIES_BUTTON_LOCATOR)
        for category in categories:
            category_checkbox = self.browser.find_element(
                f'//input[@type="checkbox" and contains(@value, "{category}")]'
            )
            if not category_checkbox.is_selected():
                category_checkbox.click()

    def accept_cookies(self):
        self.browser.click_button_when_visible(self._COOKIES_BUTTON_LOCATOR)

    @property
    def exists_show_more_button(self):
        return self.browser.is_element_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _filter_articles_by_end_date(self, articles: list, end_date: date):
        filtered_news = []
        for news in articles:
            if (news['date'].month, news['date'].year) >= (end_date.month, end_date.year):
                filtered_news.append(news)
        return filtered_news

    def _has_articles_reached_end_date(self, all_articles: list, end_date):
        return any((
            article['date'].month == end_date.month
            and article['date'].year == end_date.year
            for article in all_articles
        ))

    def _get_article_title(self, article: WebElement):
        return self.browser.find_element(
            self._ARTICLE_TITLE_LOCATOR, article
        ).text

    def _get_article_description(self, article: WebElement) -> str:
        if self.browser.does_page_contain_element(
            self._ARTICLE_DESCRIPTION_LOCATOR
        ):
            return self.browser.find_element(self._ARTICLE_DESCRIPTION_LOCATOR,
                                             article).text
        return ''

    def _get_image_url(self, article: WebElement) -> str:
        try:
            return self.browser.find_element("css:img",
                                             article).get_attribute("src")
        except ElementNotFound:
            return ''

    def _click_show_more_button(self):
        self.browser.click_button_when_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _get_date(self, article: WebElement) -> date:
        article_date = (
            self.browser.find_element("css:span", article)
            .get_attribute('aria-label')
        )
        return self._convert_date(article_date)

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
