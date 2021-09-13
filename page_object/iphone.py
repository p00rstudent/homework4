from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.base import BaseOpenCartPage


class IphonePage(BaseOpenCartPage):
    PRODUCT = (By.CSS_SELECTOR, '#product-product')
    TITLE = (By.TAG_NAME, 'h1')
    DESCRIPTION = (By.CSS_SELECTOR, '#tab-description')

    def __init__(self, base_url: str, driver: webdriver):
        super().__init__(driver)
        self._url = base_url + '/iphone'

    def check(self):
        self.load()
        for element in (
                self.PRODUCT,
                self.TITLE,
                self.DESCRIPTION
        ):
            self.check_element(element)
