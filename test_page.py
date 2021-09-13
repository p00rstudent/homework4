from random import choice, randint

import allure
import pytest
from selenium.webdriver.common.by import By


@allure.title("Check elements on pages")
def test_pages_check(main_page, register_page, login_page, iphone_page, admin_page):
    for page in (main_page, register_page, login_page, iphone_page, admin_page):
        with allure.step(f'Check {page}'):
            page.check()


@allure.title("Check changes of currencies on main page")
def test_change_currency(main_page):
    main_page.load()
    for currency in main_page.top_container.CURRENCIES:
        with allure.step(f'Check {currency}'):
            main_page.top_container.change_currency(currency)
            assert main_page.top_container.currency == main_page.top_container.CURRENCIES[currency]


def test_account_registration(register_page):
    register_page.register_account(account=generate_account())


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


def test_login_warning(login_page):
    login_page.check_login_warning()


#@allure.title(f'Check count of elements on iphone_page, {element}')
@pytest.mark.parametrize('element',
                         [
                             ((By.CSS_SELECTOR, 'li'), 76),
                             ((By.CSS_SELECTOR, 'div'), 59),
                             ((By.CSS_SELECTOR, 'script'), 12)
                         ])
def test_check_iphone_elements_count(browser, iphone_page, element):
    iphone_page.load()
    assert iphone_page.get_elements_count(element[0]) == element[1]


#@allure.title(f'Check product addition and deletion, product: {product}, admin account: {account}')
@pytest.mark.parametrize('account', [{'username': 'user', 'password': 'bitnami'}])
@pytest.mark.parametrize('product', [{'name': 'name', 'meta_title': 'title', 'model': 'model'}])
def test_admin_page_add_and_delete_product(admin_page, account, product):
    with allure.step(f'Login into admin account'):
        admin_page.login(account)
    with allure.step(f'Add product'):
        admin_page.add_product(product)
    with allure.step(f'Find product'):
        admin_page.filter_product_by_name(product['name'])
    assert admin_page.filter_product_count() == 1
    with allure.step(f'Delete product'):
        with allure.step(f'Select product'):
            admin_page.click_filter_checkbox_by_index(0)
            with allure.step(f'Delete selected product'):
                admin_page.delete_selected_product()
