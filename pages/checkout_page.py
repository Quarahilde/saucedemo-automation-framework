from playwright.sync_api import Page
from .base_page import BasePage


class CheckoutPage(BasePage):

    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    FIRST_NAME = "[data-test='firstName']"
    LAST_NAME = "[data-test='lastName']"
    POSTAL_CODE = "[data-test='postalCode']"
    CART_LINK = "[data-test='shopping-cart-link']"
    ERROR_MESSAGE = "[data-test='error']"



    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/checkout-step-one.html"


    def fill_in_details(self, first_name: str, last_name: str, postal_code: str):
        self.page.locator(self.FIRST_NAME).fill(first_name)
        self.page.locator(self.LAST_NAME).fill(last_name)
        self.page.locator(self.POSTAL_CODE).fill(postal_code)

    def continue_checkout(self):
        self.page.locator(self.CONTINUE_BUTTON).click()

    def cancel_checkout(self):
        self.page.locator(self.CANCEL_BUTTON).click()

    def go_back_to_cart(self):
        self.page.locator(self.CART_LINK).click()

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).text_content()
    
    def is_error_visible(self) -> bool:
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
    
    def fill_firstname(self, first_name: str):
        self.page.locator(self.FIRST_NAME).fill(first_name)

    def fill_lastname(self, last_name: str):
        self.page.locator(self.LAST_NAME).fill(last_name)

    def fill_postal_code(self, postal_code: str):
        self.page.locator(self.POSTAL_CODE).fill(postal_code)