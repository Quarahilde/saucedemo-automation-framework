from playwright.sync_api import Page
from .base_page import BasePage



class ProductsPage(BasePage):

    PRODUCT = "[data-test='inventory-item']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    CART_LINK = "[data-test='shopping-cart-link']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    PRODUCT_SORT = "[data-test='product-sort-container']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/inventory.html"
    
    # Action Methods - do something

    def add_product_to_cart_by_index(self, index: int):
      all_products = self.page.locator(self.PRODUCT)
      product = all_products.nth(index)
      button = product.locator("button")
      if button.text_content() == "Add to cart":
        button.click()
      else:
         raise ValueError(f"Invalid index: {index}, or product with index:{index} has already been added.")

    def add_product_to_cart_by_name(self, name: str):
       all_products = self.page.locator(self.PRODUCT)

       for i in range(all_products.count()):
          
          product = all_products.nth(i)

          product_name = product.locator(self.PRODUCT_NAME).text_content()

          if product_name == name:
            button = product.locator("button")
            if button.text_content() == "Add to cart":
              button.click()
              return
       raise ValueError(f"Product {name} not found.")


    def remove_product_from_cart_by_index(self, index: int):
      all_products = self.page.locator(self.PRODUCT)
      product = all_products.nth(index)
      button = product.locator("button")
      if button.text_content() == "Remove":
         button.click()
      else:
         raise ValueError(f"Product at index {index} is not in cart")
          
    def go_to_cart(self):
      self.page.locator(self.CART_LINK).click()

    def sort_products(self, option: str):

      valid_options = ['az', 'za', 'hilo', 'lohi']

      if option not in valid_options:
         raise ValueError(
            f"Invalid sort option: {option}. "
            f"Valid options are {', '.join(valid_options)}"
         )
      
      self.page.locator(self.PRODUCT_SORT).select_option(option)

      
    def get_product_count(self) -> int:
      return self.page.locator(self.PRODUCT).count()
    
    def get_cart_badge_count(self) -> str:
      badge = self.page.locator(self.CART_BADGE)

      if badge.is_visible():
        return badge.text_content()
      else: 
        return "0"

  
    def get_all_product_names(self) -> list[str]:
      product_names_list = []
      all_products = self.page.locator(self.PRODUCT)
      for i in range(all_products.count()):
        product = all_products.nth(i)

        product_name = product.locator(self.PRODUCT_NAME).text_content()
        product_names_list.append(product_name)

      return product_names_list
    
    def get_all_product_prices(self) -> list[float]:
      product_prices_list = []
      all_price_elements = self.page.locator(self.PRODUCT_PRICE)

      for i in range(all_price_elements.count()):
        price_text = all_price_elements.nth(i).text_content()
        price_clean = price_text.replace("$", "")
        price_float = float(price_clean)
        
        product_prices_list.append(price_float)
      return product_prices_list
    
    def is_product_in_cart(self, name: str) -> bool:
      all_products = self.page.locator(self.PRODUCT)

      for i in range(all_products.count()):
         
        product = all_products.nth(i)
        product_name = product.locator(self.PRODUCT_NAME).text_content()

        if product_name == name:
          if product.locator("button").text_content() == "Remove":
            return True
          else:
            return False
      
      raise ValueError(f"Product {name} not found.")
           