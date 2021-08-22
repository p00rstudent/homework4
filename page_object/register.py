from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.base import BaseOpenCartPage


class RegisterPage(BaseOpenCartPage):
    FIRSTNAME = (By.CSS_SELECTOR, '#input-firstname')
    LASTNAME = (By.CSS_SELECTOR, '#input-lastname')
    EMAIL = (By.CSS_SELECTOR, '#input-email')
    TELEPHONE = (By.CSS_SELECTOR, '#input-telephone')
    PASSWORD = (By.CSS_SELECTOR, '#input-password')
    CONFIRM = (By.CSS_SELECTOR, '#input-confirm')
    AGREE = (By.CSS_SELECTOR, "input[name='agree']")
    CONTINUE = (By.CSS_SELECTOR, "input[value='Continue']")
    CREATED = (By.XPATH, "//h1[contains(text(), 'Your Account Has Been Created!')]")

    def __init__(self, base_url: str, driver: webdriver):
        super().__init__(driver)
        self._url = base_url + '/index.php?route=account/register'

    def register_account(self, account: dict):
        if self.driver.current_url != self.url:
            self.load()
        self.check()
        self.insert_text_by_locator(self.FIRSTNAME, account['firstname'])
        self.insert_text_by_locator(self.LASTNAME, account['lastname'])
        self.insert_text_by_locator(self.EMAIL, account['email'])
        self.insert_text_by_locator(self.TELEPHONE, account['telephone'])
        self.insert_text_by_locator(self.PASSWORD, account['password'])
        self.insert_text_by_locator(self.CONFIRM, account['password'])
        self.click_by_locator(self.AGREE)
        self.click_by_locator(self.CONTINUE)
        self.check_element(self.CREATED)

    def check(self):
        self.load()
        for locator in (
                self.FIRSTNAME,
                self.LASTNAME,
                self.EMAIL,
                self.TELEPHONE,
                self.PASSWORD,
                self.CONFIRM,
                self.AGREE,
                self.CONTINUE
        ):
            self.check_element(locator)
