from pathlib import Path

import pytest
from selenium import webdriver

from page_object.admin import AdminPage
from page_object.iphone import IphonePage
from page_object.main import MainPage
from page_object.page_element.login import LoginPage
from page_object.register import RegisterPage

DRIVERS_DIRECTORY = Path(__file__).parent.parent.joinpath('drivers')


def driver_factory(browser):
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=DRIVERS_DIRECTORY.joinpath('chromedriver'))
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=DRIVERS_DIRECTORY.joinpath('geckodriver'))
    elif browser == 'opera':
        driver = webdriver.Opera(executable_path=DRIVERS_DIRECTORY.joinpath('operadriver'))
    else:
        raise Exception('Driver not supported')
    return driver


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome', type=str, choices='chrome, firefox, opera')
    parser.addoption('--opencart_url', default='http://172.24.113.3:8081/')
    parser.addoption('--wait_timeout', type=float, default=5)
    parser.addoption('--poll_frequency', type=float, default=0.5)


@pytest.fixture
def browser(request):
    driver = driver_factory(request.config.getoption('--browser'))
    driver.maximize_window()
    request.addfinalizer(driver.quit)
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
