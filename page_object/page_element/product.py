from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.page_element.element.element import Element


class Product(Element):
    IMAGE = (By.CLASS_NAME, '#image')
    ADD_TO_CARD = (By.XPATH, "//button[contains(@onclick,'cart.add')]")
    ADD_TO_WISH = (By.XPATH, "//button[contains(@onclick,'wishlist.add')]")
    ADD_TO_COMPARE = (By.XPATH, "//button[contains(@onclick,'wishlist.add')]")

    def __init__(self, root_element, driver: webdriver):
        super().__init__(driver)
        self.root = root_element

    def add_to_card(self):
        return self.click_by_locator(self.ADD_TO_CARD)

    def add_to_wish(self):
        return self.click_by_locator(self.ADD_TO_WISH)

    def add_to_compare(self):
        return self.click_by_locator(self.ADD_TO_COMPARE)
