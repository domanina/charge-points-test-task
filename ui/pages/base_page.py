import urllib.parse
from abc import ABC

from playwright.sync_api import Page


DEFAULT_TIMEOUT = 5000


class BasePage(ABC):

    URL = None
    EXPECTED_TITLE = None
    PAGE_TITLE_SELECTOR = None

    def __init__(self, page: Page):
        self.page = page
        self.locator = self.page.locator
        self.page.set_default_timeout(DEFAULT_TIMEOUT)

    def goto(self, dynamic_url_postfix=None, **kwargs):
        if self.URL:
            url = self.URL + (dynamic_url_postfix or "")
            if kwargs:
                url += f"?{urllib.parse.urlencode(kwargs)}"
            self.page.goto(url, timeout=DEFAULT_TIMEOUT * 2)
            return self
        else:
            raise NotImplementedError(f"Url is not set {self.__class__.__name__}")
