import logging
from pathlib import Path

import pytest
from selenium import webdriver

from page_object.admin import AdminPage
from page_object.iphone import IphonePage
from page_object.main import MainPage
from page_object.page_element.login import LoginPage
from page_object.register import RegisterPage

DRIVERS_DIRECTORY = Path(__file__).parent.parent.joinpath('drivers')
LOGS_DIRECTORY = Path(__file__).parent.joinpath('logs')
LOGS_DIRECTORY.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, filename="logs/selenium.log")


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome', type=str, choices='chrome, firefox, opera')
    parser.addoption("--bversion", action="store", default="92.0")
    parser.addoption("--executor", action="store", default="localhost")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption('--opencart_url', default='http://172.24.113.3:8081/')
    parser.addoption('--wait_timeout', type=float, default=5)
    parser.addoption('--poll_frequency', type=float, default=0.5)


def driver_factory(request):
    browser = request.config.getoption('--browser')
    executor = request.config.getoption('--executor')
    if executor == 'localhost':
        if browser == 'chrome':
            driver = webdriver.Chrome(executable_path=DRIVERS_DIRECTORY.joinpath('chromedriver'))
        elif browser == 'firefox':
            driver = webdriver.Firefox(executable_path=DRIVERS_DIRECTORY.joinpath('geckodriver'))
        elif browser == 'opera':
            driver = webdriver.Opera(executable_path=DRIVERS_DIRECTORY.joinpath('operadriver'))
        else:
            raise Exception('Driver not supported')

    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            "browserName": browser,
            "browserVersion": request.config.getoption('--bversion'),
            "screenResolution": "1280x1024",
            "name": "agr tests",
            "selenoid:options": {
                "sessionTimeout": "60s",
                "enableVNC": request.config.getoption('--vnc'),
                "enableVideo": request.config.getoption('--videos'),
                "enableLog": request.config.getoption('--logs')
            }
        }
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=caps)
    return driver


@pytest.fixture
def browser(request):
    driver = driver_factory(request)
    driver.maximize_window()

    def fin():
        allure_dir = Path(__file__).parent.joinpath('allure-results')
        allure_dir.mkdir(exist_ok=True)
        allure_dir.joinpath('environment.properties').write_text(f"Browser={request.config.getoption('--browser')}\nBrowser.Version={request.config.getoption('--bversion')}\nExecutor={request.config.getoption('--executor')}\n")
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture
def opencart_url(request):
    return request.config.getoption('--opencart_url')


@pytest.fixture
def main_page(request, browser):
    return MainPage(driver=browser, base_url=request.config.getoption('--opencart_url'))


@pytest.fixture
def register_page(request, browser):
    return RegisterPage(driver=browser, base_url=request.config.getoption('--opencart_url'))


@pytest.fixture
def login_page(request, browser):
    return LoginPage(driver=browser, base_url=request.config.getoption('--opencart_url'))


@pytest.fixture
def iphone_page(request, browser):
    return IphonePage(driver=browser, base_url=request.config.getoption('--opencart_url'))


@pytest.fixture
def admin_page(request, browser):
    return AdminPage(driver=browser, base_url=request.config.getoption('--opencart_url'))
