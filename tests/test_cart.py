from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
import pytest



def test_remove_product_from_cart_by_name(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    assert cart_page.get_cart_item_count() == 1
    assert cart_page.is_product_in_cart("Sauce Labs Backpack")
    cart_page.remove_product_by_name("Sauce Labs Backpack")
    assert cart_page.get_cart_item_count() == 0
    assert not cart_page.is_product_in_cart("Sauce Labs Backpack")
    
def test_remove_product_from_cart_by_index(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    assert cart_page.get_cart_item_count() == 1
    cart_page.remove_product_by_index(0)
    assert cart_page.get_cart_item_count() == 0
    assert cart_page.is_cart_empty()

def test_continue_shopping(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.go_to_cart()
    cart_page.continue_shopping()
    expect(logged_in_page).to_have_url(products_page.url)
    
def test_proceed_checkout(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.proceed_to_checkout()
    checkout_title = logged_in_page.locator("[data-test='title']")
    expect(checkout_title).to_have_text("Checkout: Your Information")

def test_get_cart_item_count(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    for i in range(3):
        products_page.add_product_to_cart_by_index(i)
    products_page.go_to_cart()
    count = cart_page.get_cart_item_count()
    assert count == 3

def test_is_cart_empty_when_empty(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.go_to_cart()
    assert cart_page.is_cart_empty()

def test_is_cart_empty_when_has_items(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    for i in range(2):
        products_page.add_product_to_cart_by_index(i)
    products_page.go_to_cart()
    assert not cart_page.is_cart_empty()

def test_is_product_in_cart_returns_true(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    assert cart_page.is_product_in_cart("Sauce Labs Backpack")

def test_is_product_in_cart_returns_false(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    assert not cart_page.is_product_in_cart("Sauce Labs Bike Light")

def test_get_cart_item_names(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
    products_page.go_to_cart()
    names = cart_page.get_cart_item_names()
    assert all(p in names for p in ["Sauce Labs Backpack", "Sauce Labs Bike Light"])
    assert len(names) == 2

def test_get_product_quantity(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    names = cart_page.get_cart_item_names()
    qty = cart_page.get_product_quantity(names[0])
    assert qty == 1

def test_remove_multiple_products(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    for i in range(3):
        products_page.add_product_to_cart_by_index(i)
    products_page.go_to_cart()
    assert cart_page.get_cart_item_count() == 3
    cart_page.remove_product_by_index(0)
    assert cart_page.get_cart_item_count() == 2
    cart_page.remove_product_by_index(0)
    assert cart_page.get_cart_item_count() == 1

def test_remove_product_by_invalid_name_fails(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    with pytest.raises(ValueError):
        cart_page.remove_product_by_name("Nonexistent Product")
    
def test_remove_product_by_invalid_index_fails(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    with pytest.raises(ValueError):
        cart_page.remove_product_by_index(5)

def test_get_product_quantity_invalid_name_fails(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    with pytest.raises(ValueError):
        cart_page.get_product_quantity("Nonexistent Product")

def test_cart_persists_after_continue_shopping(logged_in_page: Page):
    cart_page = CartPage(logged_in_page)
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    products_page.go_to_cart()
    cart_page.continue_shopping()
    assert products_page.get_cart_badge_count() == "1"