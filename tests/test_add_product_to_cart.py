import requests
from allure_commons._allure import step
from selene import browser
from selene.support.conditions import have
from utils import attach

API_URL = "https://demowebshop.tricentis.com/addproducttocart"
CART_URL = "https://demowebshop.tricentis.com/cart"


def test_add_one_product_to_cart():
    url = API_URL + "/details/72/1"
    EnteredQuantity = 5

    payload = {
        "product_attribute_72_5_18": 53,
        "product_attribute_72_6_19": 54,
        "product_attribute_72_3_20": 57,
        "addtocart_72.EnteredQuantity": EnteredQuantity
    }

    with step("Add product to cart by post request"):
        response = requests.post(url=url, data=payload)
        attach.request_url_and_body(response)
        attach.response_json_and_cookies(response)
        attach.logging_response(response)

    with step("Get cookie from post request"):
        cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from post request"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("Verify amount in the cart"):
        attach.add_screenshot(browser)
        browser.element(".cart-qty").should(have.text(f"({EnteredQuantity})"))


def test_add_two_products_to_cart():
    books_url = API_URL + "/details/"
    id_first_book = 45
    id_second_book = 22
    EnteredQuantity_first_book = 5
    EnteredQuantity_second_book = 10

    payload_fiction = {
        f"addtocart_{id_first_book}.EnteredQuantity": EnteredQuantity_first_book
    }

    payload_health = {
        f"addtocart_{id_second_book}.EnteredQuantity": EnteredQuantity_second_book
    }

    with step("Add first book to cart by post request"):
        response_first_book = requests.post(url=books_url + f'{id_first_book}/1', data=payload_fiction)
        attach.request_url_and_body(response_first_book)
        attach.response_json_and_cookies(response_first_book)
        attach.logging_response(response_first_book)

    with step("Add second book to cart by post request"):
        response_second_book = requests.post(url=books_url + f'{id_second_book}/1', data=payload_health,
                                             cookies=response_first_book.cookies)
        attach.request_url_and_body(response_second_book)
        attach.response_json_and_cookies(response_second_book)
        attach.logging_response(response_second_book)

    with step("Get cookie from post request"):
        cookie = response_second_book.cookies.get("Nop.customer")

    with step("Set cookie from post request"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("Verify amount in the cart"):
        attach.add_screenshot(browser)
        browser.element(".cart-qty").should(have.text(f"({EnteredQuantity_first_book + EnteredQuantity_second_book})"))
