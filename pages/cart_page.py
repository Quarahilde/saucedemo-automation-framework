from playwright.sync_api import Page
from .base_page import BasePage



class CartPage(BasePage):

    PRODUCT = "[data-test='inventory-item']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_DESC = "[data-test='inventory-item-desc']"
    PRODUCT_QTY = "[data-test='item-quantity']"
    CONTINUE_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CART_TITLE = "[data-test='title']"
     

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/cart.html"

    def remove_product_by_index(self, index: int):
        """Remove product from cart by position"""
        all_products = self.page.locator(self.PRODUCT)
        if not (0 <= index < all_products.count()):
            raise ValueError(f"There is no product at index: {index}.")
 
        product = all_products.nth(index)
        button = product.locator("button")
        button.click()

    def remove_product_by_name(self, name: str):
        """Remove product from cart by name"""
        all_products = self.page.locator(self.PRODUCT)
        for i in range(all_products.count()):
            product = all_products.nth(i)
            product_name = product.locator(self.PRODUCT_NAME).text_content()
            if product_name == name:
                remove_btn = product.locator("button")
                remove_btn.click()
                return
        else:
            raise ValueError(f"Product of name:'{name}' doesn't exist.")
    
    def continue_shopping(self):
        """Click Continue Shopping button"""
        self.page.locator(self.CONTINUE_BUTTON).click()
    
    def proceed_to_checkout(self):
        """Click Checkout button"""
        self.page.locator(self.CHECKOUT_BUTTON).click()
    
    # Getter methods
    def get_cart_item_count(self) -> int:
        """Return number of items in cart"""
        return self.page.locator(self.PRODUCT).count()

    def get_cart_item_names(self) -> list[str]:
        """Return list of all product names in cart"""
        names = []
        all_products = self.page.locator(self.PRODUCT)
        for i in range(all_products.count()):
            product = all_products.nth(i)
            product_name = product.locator(self.PRODUCT_NAME).text_content()
            names.append(product_name)
        return names

    def get_product_quantity(self, name: str) -> int:
        """Return quantity of specific product"""
        all_products = self.page.locator(self.PRODUCT)
        for i in range(all_products.count()):
            product = all_products.nth(i)
            product_name = product.locator(self.PRODUCT_NAME).text_content()

            if name == product_name:
                count = product.locator(self.PRODUCT_QTY).text_content()
                return int(count)
        else:
            raise ValueError(f"Product of name:'{name}' doesn't exist.")
    
    def is_cart_empty(self) -> bool:
        """Check if cart has no items"""
        return self.page.locator(self.PRODUCT).count() == 0
    
    def is_product_in_cart(self, name: str) -> bool:
        """Check if product is in cart"""
        all_products = self.page.locator(self.PRODUCT)

        for i in range(all_products.count()):
            product = all_products.nth(i)
            product_name = product.locator(self.PRODUCT_NAME).text_content().strip()

            if product_name == name:
                return True
            
        return False