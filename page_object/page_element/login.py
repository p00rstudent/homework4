from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.base import BaseOpenCartPage


class LoginPage(BaseOpenCartPage):
    EMAIL = (By.CSS_SELECTOR, '#input-email')
    PASSWORD = (By.CSS_SELECTOR, '#input-password')
    LOGIN = (By.CSS_SELECTOR, "input[value='Login']")
    FORGOT = (By.LINK_TEXT, 'Forgotten Password')
    WARNING = (By.XPATH, "//div[contains(text(),' Warning: No match for E-Mail Address and/or Password.')]")

    def __init__(self, base_url: str, driver: webdriver):
        super().__init__(driver)
        self._url = base_url + '/index.php?route=account/login'

    def login(self, account: dict):
        if self.driver.current_url != self.url:
            self.load()
        self.check()
        self.insert_text_by_locator(self.EMAIL, account['email'])
        self.insert_text_by_locator(self.PASSWORD, account['password'])
        self.click_by_locator(self.LOGIN)

    def check(self):
        self.load()
        for locator in (
                self.EMAIL,
                self.PASSWORD,
                self.LOGIN,
                self.FORGOT
        ):
            self.check_element(locator)

    def check_login_warning(self):
        if self.driver.current_url != self.url:
            self.load()
        self.clear_by_locator(self.EMAIL)
        self.clear_by_locator(self.PASSWORD)
        self.click_by_locator(self.LOGIN)
        self.check_element(self.WARNING)
