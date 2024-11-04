from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com/"
        self.COMPANY_MENU = (By.XPATH, '//li[@class="nav-item dropdown"]//a[contains(text(),"Company")]')
        self.CAREERS_SUBMENU = (By.XPATH, '//li[@class="nav-item dropdown show"]//div//a[contains(text(),"Careers")]')

    def open_home_page(self):
        self.open_page(self.url)
        return self

    def open_careers_page(self):
        self.click_element(self.COMPANY_MENU)
        self.wait_for_element_to_be_clickable(self.CAREERS_SUBMENU)
        self.click_element(self.CAREERS_SUBMENU)
        return self

    def accept_cookies(self):
        try:
            accept_button = (By.XPATH, '//a[@id="wt-cli-accept-btn" and text()="Only Necessary"]')
            self.wait_for_element_to_be_clickable(accept_button)
            self.driver.find_element(*accept_button).click()
        except Exception as e:
            print(f"No cookies accept button found: {e}")