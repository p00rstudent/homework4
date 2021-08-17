from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from page_object.page_object import PageObject

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
def timeout(request):
    return request.config.getoption('--wait_timeout')


@pytest.fixture
def poll_frequency(request):
    return request.config.getoption('--poll_frequency')


@pytest.fixture
def opencart_url(request):
    return request.config.getoption('--opencart_url')


@pytest.fixture
def mainpage(request):
    return PageObject(url=request.config.getoption('--opencart_url'),
                      elements={
                          'title': (By.CSS_SELECTOR, "a[href*='route=common/home']"),
                          'search': (By.CSS_SELECTOR, "input[name='search']"),
                          'cart': (By.CSS_SELECTOR, '#cart'),
                          'common-home': (By.CSS_SELECTOR, '#common-home'),
                          'featured': (By.XPATH, "//h3[contains(text(),'Featured')]")
                      })


@pytest.fixture
def desktop_pc_page(request):
    return PageObject(url=request.config.getoption('--opencart_url') + '/desktops/pc',
                      elements={
                          'pc': (By.XPATH, "//aside//a[contains(text(),'PC')]"),
                          'mac': (By.XPATH, "//aside//a[contains(text(),'Mac')]"),
                          'laptops': (By.XPATH, "//aside//a[contains(text(),'Laptops & Notebooks')]"),
                          'components': (By.XPATH, "//aside//a[contains(text(),'Components')]"),
                          'tablets': (By.XPATH, "//aside//a[contains(text(),'Tablets')]")
                      })


@pytest.fixture
def iphone_page(request):
    return PageObject(url=request.config.getoption('--opencart_url') + '/iphone', elements={})


@pytest.fixture
def login_page(request):
    return PageObject(url=request.config.getoption('--opencart_url') + '/index.php?route=account/login',
                      elements={
                          'email': (By.CSS_SELECTOR, '#input-email'),
                          'password': (By.CSS_SELECTOR, '#input-password'),
                          'login': (By.CSS_SELECTOR, "input[value='Login']"),
                          'warning': (
                              By.XPATH,
                              "//div[contains(text(),' Warning: No match for E-Mail Address and/or Password.')]"
                          )
                      })


@pytest.fixture
def reg_user_page(request):
    return PageObject(url=request.config.getoption('--opencart_url') + '/index.php?route=account/register',
                      elements={
                          'firstname': (By.CSS_SELECTOR, '#input-firstname'),
                          'lastname': (By.CSS_SELECTOR, '#input-lastname'),
                          'email': (By.CSS_SELECTOR, '#input-email'),
                          'telephone': (By.CSS_SELECTOR, '#input-telephone'),
                          'password': (By.CSS_SELECTOR, '#input-password'),
                          'confirm': (By.CSS_SELECTOR, '#input-confirm'),
                          'agree': (By.CSS_SELECTOR, "input[name='agree']"),
                          'continue': (By.CSS_SELECTOR, "input[value='Continue']")
                      })
