from playwright.sync_api import Page, expect
from pages.login_page import LoginPage



def test_successful_login(page: Page):

    """Verify successful login"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_login_with_invalid_username(page: Page):

    """Verify error message appears with invalid username"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("invalid_user", "secret_sauce")

    error_locator = page.locator(login_page.ERROR_MESSAGE)
    expect(error_locator).to_be_visible()
    expect(error_locator).to_contain_text("do not match", ignore_case=True)


def test_login_with_invalid_passsword(page: Page):

    """Verify error appears with invalid password"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("standard_user", "wrong_password")

    error_locator = page.locator(login_page.ERROR_MESSAGE)

    expect(error_locator).to_be_visible()

    expect(error_locator).to_contain_text("do not match", ignore_case=True)

def test_login_with_locked_user(page: Page):

    """Verify locked user cannot login"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("locked_out_user", "secret_sauce")

    error_locator = page.locator(login_page.ERROR_MESSAGE)

    expect(error_locator).to_be_visible()

    expect(error_locator).to_contain_text("locked out")

def test_login_with_empty_username(page: Page):

    """Verify error appears when username is empty"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("", "secret_sauce")

    error_locator = page.locator(login_page.ERROR_MESSAGE)

    expect(error_locator).to_be_visible()

    expect(error_locator).to_contain_text("username is required", ignore_case=True)


def test_login_with_empty_password(page: Page):

    """Verify error appears when password is empty"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("standard_user", "")

    error_locator = page.locator(login_page.ERROR_MESSAGE)

    expect(error_locator).to_be_visible()

    expect(error_locator).to_contain_text("password is required", ignore_case=True)



def test_login_with_empty_credentials(page: Page):

    """Verify error appears when both fields are empty"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("", "")

    error_locator = page.locator(login_page.ERROR_MESSAGE)

    expect(error_locator).to_be_visible()

    expect(error_locator).to_contain_text("username is required", ignore_case=True)




def test_login_with_problem_user(page: Page):

    """Verify problem user can login successfully"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("problem_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")



def test_login_with_performance_glitch_user(page: Page):

    """Verify performance glitch user can login successfully"""

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("performance_glitch_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")