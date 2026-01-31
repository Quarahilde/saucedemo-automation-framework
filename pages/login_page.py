from playwright.sync_api import Page
from .base_page import BasePage



class LoginPage(BasePage):

    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://saucedemo.com/"
    
    def navigate(self):

        self.navigate_to(self.url)

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self):
        return self.is_visible(self.ERROR_MESSAGE)
        