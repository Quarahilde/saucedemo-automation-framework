from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
import pytest


def test_fill_checkout_details_and_continue(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_in_details("Mariusz", "Danielak", "test")
    checkout_page.continue_checkout()
    expect(logged_in_page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

def test_cancel_checkout_returns_to_cart(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.cancel_checkout()
    expect(logged_in_page).to_have_url(cart_page.url)

def test_cart_link_from_checkout(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)  
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.go_back_to_cart()
    expect(logged_in_page).to_have_url(cart_page.url)

def test_checkout_with_empty_first_name(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_lastname("Danielak")
    checkout_page.fill_postal_code("test")
    checkout_page.continue_checkout()
    assert checkout_page.is_error_visible()
    assert checkout_page.get_error_message() == "Error: First Name is required"

def test_checkout_with_empty_last_name(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_firstname("Mariusz")
    checkout_page.fill_postal_code("test")
    checkout_page.continue_checkout()
    assert checkout_page.is_error_visible()
    assert checkout_page.get_error_message() == "Error: Last Name is required"

def test_checkout_with_empty_postal_code(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_firstname("Mariusz")
    checkout_page.fill_lastname("Danielak")
    checkout_page.continue_checkout()
    assert checkout_page.is_error_visible()
    assert checkout_page.get_error_message() == "Error: Postal Code is required"


def test_checkout_with_all_empty_fields(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.continue_checkout()
    assert checkout_page.is_error_visible()

def test_individual_field_filling(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_firstname("Mariusz")
    assert logged_in_page.locator(checkout_page.FIRST_NAME).input_value() == "Mariusz"
    checkout_page.fill_lastname("Danielak")
    assert logged_in_page.locator(checkout_page.LAST_NAME).input_value() == 'Danielak'
    checkout_page.fill_postal_code("test")
    assert logged_in_page.locator(checkout_page.POSTAL_CODE).input_value() == "test"
