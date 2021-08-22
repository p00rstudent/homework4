from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_object.base import BaseOpenCartPage


class AdminPage(BaseOpenCartPage):
    USERNAME = (By.CSS_SELECTOR, '#input-username')
    PASSWORD = (By.CSS_SELECTOR, '#input-password')
    LOGIN = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOT = (By.LINK_TEXT, 'Forgotten Password')
    CATALOG = (By.CSS_SELECTOR, '#menu-catalog')
    PRODUCT_ADD = (By.XPATH, "//a[contains(@href,'catalog/product/add')]")
    PRODUCT_DELETE = (By.XPATH, "//button[contains(@formaction,'catalog/product/delete')]")
    PRODUCT_NAME = (By.CSS_SELECTOR, '#input-name1')
    PRODUCT_META_TITLE = (By.CSS_SELECTOR, '#input-meta-title1')
    SAVE_PRODUCT = (By.CSS_SELECTOR, "button[data-original-title='Save']")
    PRODUCT_DATA = (By.LINK_TEXT, 'Data')
    PRODUCT_MODEL = (By.CSS_SELECTOR, '#input-model')
    PRODUCT_SUCCESS = (By.CLASS_NAME, 'alert-success')
    PRODUCT_FILTER_NAME = (By.CSS_SELECTOR, '#input-name')
    PRODUCT_FILTER_BUTTON = (By.CSS_SELECTOR, '#button-filter')
    PRODUCT_FILTER_COUNT = (By.XPATH, '//tbody/tr')
    PRODUCT_FILTER_CHECKBOX = (By.TAG_NAME, 'input')

    def __init__(self, base_url: str, driver: webdriver):
        super().__init__(driver)
        self._url = base_url + '/admin'

    def login(self, account: dict):
        if self.driver.current_url != self.url:
            self.load()
        self.check()
        self.insert_text_by_locator(self.USERNAME, account['username'])
        self.insert_text_by_locator(self.PASSWORD, account['password'])
        self.click_by_locator(self.LOGIN)

    def check(self):
        self.load()
        for locator in (
                self.USERNAME,
                self.PASSWORD,
                self.LOGIN,
                self.FORGOT
        ):
            self.check_element(locator)

    def add_product(self, product: dict):
        self.open_products()
        self.click_by_locator(self.PRODUCT_ADD)
        self.fill_product(product)
        self.click_by_locator(self.SAVE_PRODUCT)
        self.check_element(self.PRODUCT_SUCCESS, EC.visibility_of_element_located)

    def open_products(self):
        catalog = self.find_element(self.CATALOG)
        if not self.catalog_is_active(catalog):
            catalog.click()
            sleep(1)
        assert self.catalog_is_active(catalog)
        catalog.find_element(By.LINK_TEXT, 'Products').click()

    def catalog_is_active(self, catalog=None):
        if catalog is None:
            catalog = self.find_element(self.CATALOG)
        return catalog.find_elements(By.TAG_NAME, 'a')[0].get_attribute('aria-expanded')

    def fill_product(self, product: dict):
        self.insert_text_by_locator(self.PRODUCT_NAME, product['name'])
        self.insert_text_by_locator(self.PRODUCT_META_TITLE, product['meta_title'])
        self.click_by_locator(self.PRODUCT_DATA)
        self.insert_text_by_locator(self.PRODUCT_MODEL, product['model'])

    def filter_product_by_name(self, name):
        self.insert_text_by_locator(self.PRODUCT_FILTER_NAME, name)
        self.click_by_locator(self.PRODUCT_FILTER_BUTTON)

    def filter_product_count(self):
        return self.get_elements_count(self.PRODUCT_FILTER_COUNT)

    def click_filter_checkbox_by_index(self, index: int):
        tr_element = self.find_elements(self.PRODUCT_FILTER_COUNT)[index]
        tr_element.find_element(*self.PRODUCT_FILTER_CHECKBOX).click()

    def delete_selected_product(self):
        self.click_by_locator(self.PRODUCT_DELETE)
        self.driver.switch_to.alert.accept()
