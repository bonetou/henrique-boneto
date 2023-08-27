from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import ElementNotFound
from news import News
from selenium.webdriver.remote.webelement import WebElement
from datetime import date


class SearchPageHandler:
    _SORT_BY_SELECT_LOCATOR = (
        '//*[@id="site-content"]/div[1]/div[1]/div[1]/form/div[2]/div/select'
    )
    _CATEGORIES_BUTTON_LOCATOR = (
        "//button[@data-testid='search-multiselect-button']"
    )
    _COOKIES_BUTTON_LOCATOR = '//button[@data-testid="GDPR-accept"]'
    _SEARCH_RESULTS_LOCATOR = "//li[@data-testid='search-bodega-result']"
    _NEWS_TITLE_LOCATOR = "css:h4"
    _NEWS_DESCRIPTION_LOCATOR = "css:a"
    _SHOW_MORE_BUTTON_LOCATOR = (
        "//button[@data-testid='search-show-more-button']"
    )
    _NEWS_DATE_LOCATOR = "css:span"

    def __init__(self, browser: Selenium):
        self.browser = browser

    def get_news_until(self, end_date: date) -> list[News]:
        while (
            self.exists_show_more_button
            and not self._news_reached_end_date(
                self.get_news(), end_date,
            )
        ):
            self._click_show_more_button()
        return self._filter_news_greater_than_end_date(self.get_news(),
                                                       end_date)

    def get_news(self) -> list[News]:
        article_results = self.browser.find_elements(
            self._SEARCH_RESULTS_LOCATOR
        )
        return [
            News(
                title=self._get_article_title(article),
                description=self._get_article_description(article),
                date=self._get_date(article),
                image_url=self._get_image_url(article),
            )
            for article in article_results
        ]

    def sort_by_newest(self):
        self.browser.select_from_list_by_value(
            self._SORT_BY_SELECT_LOCATOR,
            "newest",
        )

    def select_categories(self, categories: list[str]):
        categories = [category.lower() for category in categories]
        self.browser.click_button(self._CATEGORIES_BUTTON_LOCATOR)
        for category in categories:
            try:
                category_checkbox = self.browser.find_element(
                    f"//input[@type='checkbox' and contains(@value, '{category}')]"
                )
                if not category_checkbox.is_selected():
                    category_checkbox.click()
            except ElementNotFound:
                pass

    def accept_cookies(self):
        self.browser.click_button_when_visible(self._COOKIES_BUTTON_LOCATOR)

    @property
    def exists_show_more_button(self):
        return self.browser.is_element_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _filter_news_greater_than_end_date(
        self,
        news: list[News],
        end_date: date,
    ):
        return [
            news for news in news
            if (news.date.month, news.date.year) >= (end_date.month, end_date.year)
        ]

    def _news_reached_end_date(self, all_news: list[News], end_date):
        return any(
            (
                news.date.month == end_date.month
                and news.date.year == end_date.year
                for news in all_news
            )
        )

    def _get_article_title(self, article: WebElement) -> str:
        return self.browser.find_element(self._NEWS_TITLE_LOCATOR,
                                         article).text

    def _get_article_description(self, article: WebElement) -> str:
        if self.browser.does_page_contain_element(
            self._NEWS_DESCRIPTION_LOCATOR
        ):
            return self.browser.find_element(self._NEWS_DESCRIPTION_LOCATOR,
                                             article).text
        return ""

    def _get_image_url(self, article: WebElement) -> str:
        try:
            return (
                self.browser.find_element("css:img", article)
                .get_attribute("src")
            )
        except ElementNotFound:
            return ""

    def _click_show_more_button(self):
        self.browser.click_button_when_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _get_date(self, article: WebElement) -> str:
        return (
            self.browser.find_element(self._NEWS_DATE_LOCATOR, article)
            .get_attribute("aria-label")
        )
