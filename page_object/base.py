from page_object.page_element.element.element import Element
from page_object.page_element.top_container import TopContainer


class BasePage(Element):
    _url = None

    @property
    def url(self):
        return self._url

    def load(self):
        self.logger.info(f'Loading url: {self.url}')
        return self.driver.get(self.url)


class BaseOpenCartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._top_container = TopContainer(driver)

    @property
    def top_container(self):
        return self._top_container
