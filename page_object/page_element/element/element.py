from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Element:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def check_element(self,
                      locator,
                      method=EC.presence_of_element_located,
                      timeout=10,
                      poll_frequency=0.5,
                      ignored_exceptions=None):
        wait = WebDriverWait(self.driver, timeout, poll_frequency, ignored_exceptions)
        try:
            wait.until(method(locator))
        except TimeoutException:
            raise AssertionError(f'Wait until timeout, element: {locator}')

    def find_element(self, locator: tuple, time: float = 10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator: tuple, time: float = 10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def click_by_locator(self, locator):
        element = self.find_element(locator)
        ActionChains(self.driver).pause(0.3).move_to_element(element).click().perform()

    def insert_text_by_locator(self, locator, text):
        self.click_by_locator(locator=locator)
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def clear_by_locator(self, locator):
        self.find_element(locator).clear()

    def get_elements_count(self, locator):
        return len(self.find_elements(locator))
