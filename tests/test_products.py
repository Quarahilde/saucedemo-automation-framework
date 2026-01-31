from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
import pytest



def test_product_count(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    product_count = products_page.get_product_count()
    assert product_count == 6

def test_get_all_product_names(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    list_of_products = products_page.get_all_product_names()
    assert list_of_products[0] == "Sauce Labs Backpack"
    assert len(list_of_products) == 6

def test_get_all_product_prices(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    list_of_prices = products_page.get_all_product_prices()
    assert len(list_of_prices) == 6
    assert all(isinstance(p, float) for p in list_of_prices)
    assert all(p > 0 for p in list_of_prices)

def test_add_product_by_index(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    cart_badge_count = products_page.get_cart_badge_count()
    assert cart_badge_count == "1"

def test_add_product_by_name(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    cart_badge_count = products_page.get_cart_badge_count()
    assert cart_badge_count == "1"
    assert products_page.is_product_in_cart("Sauce Labs Backpack")
    
def test_add_multi_products(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    for i in range(3):
        products_page.add_product_to_cart_by_index(i)

    cart_badge_count = products_page.get_cart_badge_count()
    assert cart_badge_count == "3"

def test_add_same_product_twice(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    with pytest.raises(ValueError):
        products_page.add_product_to_cart_by_index(0)


def test_remove_product_from_cart(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(0)
    assert products_page.get_cart_badge_count() == "1"
    products_page.remove_product_from_cart_by_index(0)
    assert products_page.get_cart_badge_count() == "0"


def test_unable_to_remove_not_in_cart(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    with pytest.raises(ValueError):
        products_page.remove_product_from_cart_by_index(0)

def test_sort_az(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.sort_products("az")
    products = products_page.get_all_product_names()
    sorted_products = sorted(products)
    assert products == sorted_products

def test_sort_za(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.sort_products("za")
    products = products_page.get_all_product_names()
    sorted_products = sorted(products, reverse=True)
    assert products == sorted_products

def test_sort_lohi(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.sort_products("lohi")
    prices = products_page.get_all_product_prices()
    sorted_prices = sorted(prices)
    assert prices == sorted_prices

def test_sort_hilo(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.sort_products("hilo")
    prices = products_page.get_all_product_prices()
    sorted_prices = sorted(prices, reverse=True)
    assert prices == sorted_prices

def test_invalid_sort_option(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    with pytest.raises(ValueError):
        products_page.sort_products("invalid_option")

def test_navigate_to_cart(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_product_to_cart_by_index(4)
    product_name = logged_in_page.locator(products_page.PRODUCT).nth(4).locator(products_page.PRODUCT_NAME).text_content()
    products_page.go_to_cart()
    cart_item = logged_in_page.locator("[data-test='inventory-item-name']").filter(has_text=product_name)
    expect(logged_in_page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(cart_item).to_be_visible()
    
def test_empty_cart_zero(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    cart_badge_count = products_page.get_cart_badge_count()
    assert cart_badge_count == "0"

def test_product_not_in_cart(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    assert not products_page.is_product_in_cart("Sauce Labs Backpack")
    products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert products_page.is_product_in_cart("Sauce Labs Backpack")

def test_add_product_incorrect_name(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    with pytest.raises(ValueError):
        products_page.add_product_to_cart_by_name("Nonexistent Product")

