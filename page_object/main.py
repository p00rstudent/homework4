from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.base import BaseOpenCartPage
from page_object.page_element.product import Product


class MainPage(BaseOpenCartPage):
    COMMON_HOME = (By.CSS_SELECTOR, '#common-home')
    CONTENT = (By.CSS_SELECTOR, '#content')
    SLIDESHOW = (By.CSS_SELECTOR, '#slideshow0')
    FEATURED = (By.TAG_NAME, 'h3')
    PRODUCTS = (By.CSS_SELECTOR, '.product-layout')

    def __init__(self, base_url: str, driver: webdriver):
        super().__init__(driver)
        self._url = base_url

    def get_products(self):
        return [Product(driver=self.driver, root_element=element) for element in self.find_elements(self.PRODUCTS)]

    def check(self):
        self.load()
        for element in (
                self.COMMON_HOME,
                self.CONTENT,
                self.SLIDESHOW,
                self.FEATURED,
                self.PRODUCTS
        ):
            self.check_element(element)
        assert len(self.get_products()) == 4, 'Wrong count of products'
