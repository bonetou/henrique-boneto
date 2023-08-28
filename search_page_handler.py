from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import ElementNotFound
from news import News
from selenium.webdriver.remote.webelement import WebElement
from datetime import date


class SearchPageHandler:
    _SEARCH_RESULTS_LOCATOR = "//li[@data-testid='search-bodega-result']"
    _SORT_BY_LOCATOR = (
        "//select[@data-testid='SearchForm-sortBy']"
    )
    _CATEGORIES_BUTTON_LOCATOR = (
        "//button[@data-testid='search-multiselect-button']"
    )
    _COOKIES_BUTTON_LOCATOR = "//button[@data-testid='GDPR-accept']"
    _TITLE_LOCATOR = "css:h4"
    _INFO_LOCATOR = "css:a"
    _DATE_PAGE_LOCATOR = "//span[@data-testid='todays-date']"
    _DATE_LOCATOR = "css:span"
    _DESCRIPTION_LOCATOR = "css:p"
    _IMG_LOCATOR = "css:img"
    _SHOW_MORE_BUTTON_LOCATOR = (
        "//button[@data-testid='search-show-more-button']"
    )

    def __init__(self, browser: Selenium):
        self._browser = browser
        self._news: list[News] = []
        self._last_loaded_news: list[News] = []

    def get_news_until(self, end_date: date) -> list[News]:
        while self._should_continue_to_get_more_news(end_date):
            self._click_show_more_button()
            self.load_news()
        return self._filter_recent_news(self._news, end_date)

    def _should_continue_to_get_more_news(self, end_date: date) -> bool:
        return all((
            self.exists_show_more_button,
            not self._has_too_old_news(self._last_loaded_news, end_date),
        ))

    def load_news(self) -> list[News]:
        news_searched = self._browser.find_elements(
            self._SEARCH_RESULTS_LOCATOR
        )
        self._last_loaded_news = [
            News(
                title=self._get_news_title(news),
                description=self._get_news_description(news),
                raw_date=self._get_date(news),
                image_url=self._get_image_url(news),
            )
            for news in news_searched[len(self._news):]
        ]
        self._news.extend(self._last_loaded_news)

    def sort_by_newest(self):
        self._browser.select_from_list_by_value(
            self._SORT_BY_LOCATOR, "newest"
        )

    def select_categories(self, categories: list[str]):
        self._browser.click_button(self._CATEGORIES_BUTTON_LOCATOR)
        for category in categories:
            try:
                self._select_category(category)
            except ElementNotFound:
                pass

    def _select_category(self, category: str):
        category_checkbox = self._browser.find_element(
            f"//input[@type='checkbox' and contains(@value, '{category}')]"
        )
        if not category_checkbox.is_selected():
            category_checkbox.click()

    def accept_cookies(self):
        self._browser.click_element_when_visible(self._COOKIES_BUTTON_LOCATOR)

    @property
    def exists_show_more_button(self):
        return self._browser.is_element_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _filter_recent_news(
        self,
        news: list[News],
        end_date: date,
    ) -> list[News]:
        return [
            n for n in news
            if (n.news_date.month, n.news_date.year) >= (end_date.month, end_date.year)
        ]

    def _has_too_old_news(self, news: list[News], end_date):
        return any(
            (n.news_date.month, n.news_date.year) < (end_date.month, end_date.year)
            for n in news
        )

    def _get_news_title(self, news: WebElement) -> str:
        return self._browser.find_element(self._TITLE_LOCATOR,
                                          news).text

    def _get_news_description(self, news: WebElement) -> str:
        try:
            info = self._browser.find_element(self._INFO_LOCATOR, news)
            return self._browser.find_element(self._DESCRIPTION_LOCATOR,
                                              info).text
        except ElementNotFound:
            return ""

    def _get_image_url(self, news: WebElement) -> str:
        try:
            return (
                self._browser.find_element(self._IMG_LOCATOR, news)
                .get_attribute("src")
            )
        except ElementNotFound:
            return ""

    def _click_show_more_button(self):
        self._browser.click_button_when_visible(self._SHOW_MORE_BUTTON_LOCATOR)

    def _get_date(self, news: WebElement) -> str:
        return (
            self._browser.find_element(self._DATE_LOCATOR, news)
            .get_attribute("aria-label")
        )
