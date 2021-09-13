from selenium.webdriver.common.by import By

from page_object.page_element.element.element import Element


class TopContainer(Element):
    CURRENCY_BUTTON = (By.CSS_SELECTOR, '#form-currency')
    CURRENCIES = {
        'EUR':'€',
        'GBP':'£',
        'USD':'$',
    }
    CURRENCY_VALUE = (By.TAG_NAME, 'strong')

    def change_currency(self, name: str) -> bool:
        if name not in self.CURRENCIES:
            return False
        self.click_by_locator(self.CURRENCY_BUTTON)
        self.click_by_locator((By.CSS_SELECTOR, f"button[name='{name}']"))
        return True

    @property
    def currency(self):
        return self.find_element(self.CURRENCY_VALUE).text
