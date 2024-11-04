from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_element(self, locator):
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator))

    def wait_for_element_to_be_clickable(self, locator):
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator))

    def wait_for_visibility_of_element(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def click_element(self, locator):
        self.wait_for_element_to_be_clickable(locator)
        self.driver.find_element(*locator).click()

    def enter_text(self, locator, text):
        self.wait_for_element(locator)
        self.driver.find_element(*locator).send_keys(text)

    def get_element_text(self, locator):
        self.wait_for_element(locator)
        return self.driver.find_element(*locator).text

    def select_element_in_dropdown(self, locator, text):
        self.wait_for_element(locator)
        dropdown = self.driver.find_element(*locator)
        dropdown.select_by_visible_text(text)

    def move_to_element(self, locator):
        element = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def switch_to_new_tab(self):
        new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_tab)