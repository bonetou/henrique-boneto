from RPA.Browser.Selenium import Selenium


class HomePageHandler:
    _HOME_PAGE_URL = 'https://www.nytimes.com/'
    _TERMS_LOCATOR = "//div[@id='complianceOverlay']"
    _CONTINUE_BUTTON_LOCATOR = 'Continue'
    _SEARCH_BUTTON_LOCATOR = 'SEARCH'
    _SEARCH_INPUT_LOCATOR = '//*[@id="search-input"]/form/div/input'
    _GO_BUTTON_LOCATOR = 'Go'

    def __init__(self, browser_lib: Selenium):
        self._browser_lib = browser_lib

    def search(self, search_phrase: str):
        self._open_website()
        self._search_for(search_phrase)

    def _open_website(self):
        self._browser_lib.open_available_browser(url=self._HOME_PAGE_URL,
                                                 headless=True)
        self._browser_lib.wait_until_page_contains_element(self._TERMS_LOCATOR)
        self._browser_lib.click_button(self._CONTINUE_BUTTON_LOCATOR)

    def _search_for(self, search_phrase: str):
        self._browser_lib.click_button(self._SEARCH_BUTTON_LOCATOR)
        self._browser_lib.input_text(self._SEARCH_INPUT_LOCATOR, search_phrase)
        self._browser_lib.click_button(self._GO_BUTTON_LOCATOR)
