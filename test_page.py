from random import choice, randint

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def check_element(wait, element):
    try:
        wait.until(EC.visibility_of_element_located(element))
    except TimeoutException:
        raise AssertionError(f'Wait until timeout, element: {element}')


def test_check_mainpage(browser, mainpage, timeout, poll_frequency):
    browser.get(mainpage.url)
    wait = WebDriverWait(driver=browser, timeout=timeout, poll_frequency=poll_frequency)
    for element in mainpage.elements.values():
        check_element(wait, element)


def test_check_desktop_pc(browser, desktop_pc_page, timeout, poll_frequency):
    browser.get(desktop_pc_page.url)
    wait = WebDriverWait(driver=browser, timeout=timeout, poll_frequency=poll_frequency)
    for element in desktop_pc_page.elements.values():
        check_element(wait, element)


@pytest.mark.parametrize('element', [('li', 76), ('div', 59), ('script', 12)])
def test_check_iphone_elements_count(browser, iphone_page, element):
    browser.get(iphone_page.url)
    assert len(browser.find_elements(by=By.CSS_SELECTOR, value=element[0])) == element[1]


def test_login_warning(browser, login_page, timeout, poll_frequency):
    browser.get(login_page.url)
    wait = WebDriverWait(driver=browser, timeout=timeout, poll_frequency=poll_frequency)
    for element in [login_page.elements[key] for key in ['email', 'password', 'login']]:
        check_element(wait, element)
    browser.find_element(*login_page.elements['email']).send_keys('1')
    browser.find_element(*login_page.elements['password']).send_keys('1')
    browser.find_element(*login_page.elements['login']).click()
    try:
        wait.until(EC.visibility_of_element_located(login_page.elements['warning']))
    except TimeoutException:
        raise AssertionError(f"Warning not found: {login_page.elements['warning']}")


def test_account_registration(browser, reg_user_page, timeout, poll_frequency):
    browser.get(reg_user_page.url)
    wait = WebDriverWait(driver=browser, timeout=timeout, poll_frequency=poll_frequency)
    check_elements_on_page(wait, reg_user_page)
    fill_register_page(browser, reg_user_page)
    browser.find_element(*reg_user_page.elements['continue']).click()
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//h1[contains(text(), 'Your Account Has Been Created!')]")))
    except TimeoutException:
        raise AssertionError(f'Cant create account')


def check_elements_on_page(wait, page):
    for element in page.elements.values():
        check_element(wait, element)


def fill_register_page(browser, page):
    account = generate_account()
    for key in account:
        browser.find_element(*page.elements[key]).send_keys(account[key])
    browser.find_element(*page.elements['confirm']).send_keys(account['password'])
    browser.find_element(*page.elements['agree']).click()


def generate_account():
    chars = [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97, 123)]
    firstname = lastname = email = password = ''
    for i in range(10):
        firstname += choice(chars)
        lastname += choice(chars)
        email += choice(chars)
        password += choice(chars)
    email += '@mail.com'
    telephone = randint(111111111, 999999999)
    return {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'password': password,
        'telephone': telephone
    }
