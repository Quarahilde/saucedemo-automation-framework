from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a URL"""
        self.page.goto(url)

    def click(self, locator: str):
        """Click an element"""
        self.page.locator(locator).click()

    def fill(self, locator: str, text: str):
        """Fill an input field"""
        self.page.locator(locator).fill(text)

    def get_text(self, locator: str) -> str:
        """Get text content of an element"""
        return self.page.locator(locator).text_content()
    
    def is_visible(self, locator: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(locator).is_visible()
    
    def is_hidden(self, locator: str) -> bool:
        """Check if element is hidden"""
        return self.page.locator(locator).is_hidden()