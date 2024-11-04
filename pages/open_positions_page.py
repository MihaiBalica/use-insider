import time

from selenium.webdriver.common.by import By
from retrying import retry
from pages.base_page import BasePage


class OpenPositionsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.url = "https://useinsider.com/careers/open-positions/"
        self.header = (By.XPATH, '//h3[text()="All open positions"]')
        self.FILTER_BY_LOCATION_DROPDOWN = (By.XPATH, '//div/label[text()="Filter by Location"]/following-sibling::span//span[@class="select2-selection__arrow"]')
        self.FILTER_BY_LOCATION_INPUT = (By.XPATH, '//span//span[@class="select2-results"]//ul[@class="select2-results__options"]//li[text()="{}"]')
        self.FILTER_BY_DEPARTMENT_DROPDOWN = (By.XPATH, '//div/label[text()="Filter by Department"]/following-sibling::span//span[@class="select2-selection__arrow"]')
        self.FILTER_BY_DEPARTMENT_INPUT = (By.XPATH, '//div/label[text()="Filter by Department"]/following-sibling::span//span[text()="{}"]')
        self.POSITION_TITLE = (By.XPATH, '//section[@id="career-position-list"]//div[@class="position-list-item-wrapper bg-light"]//p[text()="{}"]')
        self.POSITION_DEPARTMENT = (By.XPATH,
                               '//section[@id="career-position-list"]//div[@class="position-list-item-wrapper bg-light"]//span[text()="{}"]')
        self.POSITION_LOCATION = (By.XPATH, '//section[@id="career-position-list"]//div[@class="position-list-item-wrapper bg-light"]//div[text()="{}"]')
        self.POSITION_VIEW_DETAILS = (By.XPATH,
                               '//section[@id="career-position-list"]//div[@class="position-list-item-wrapper bg-light"]//a[text()="View Role"]')


    def load(self):
        self.driver.get(self.url)

    def get_header(self):
        return self.driver.find_element_by_tag_name("h1").text

    # Here it is to discuss with the FE developer, to understand how the page is loading and
    # what is the best way to wait for the page to load. So I added a forced wait of 15 seconds
    # @retry(wait_fixed=10000, stop_max_attempt_number=2)
    def filter_by_location(self, location, department):
        # self.driver.refresh()
        time.sleep(15)
        self.wait_for_page_load(timeout=15)
        locator_filter_by_department = self.FILTER_BY_DEPARTMENT_INPUT[1].format(department)
        self.wait_for_visibility_of_element((By.XPATH, locator_filter_by_department), timeout=15)

        self.wait_for_visibility_of_element(self.FILTER_BY_LOCATION_DROPDOWN, timeout=15)
        self.driver.find_element(*self.FILTER_BY_LOCATION_DROPDOWN).click()
        location_input = (By.XPATH, self.FILTER_BY_LOCATION_INPUT[1].format(location))
        self.wait_for_element(location_input)
        self.driver.find_element(*location_input).click()
        position_location_locator = (By.XPATH, self.POSITION_LOCATION[1].format(location))
        self.wait_for_element(position_location_locator)

    def verify_position(self, title, department, position):
        locator = (By.XPATH, self.POSITION_TITLE[1].format(title))
        self.wait_for_visibility_of_element(locator, timeout=10)
        assert self.driver.find_element(*locator).is_displayed(), f"Expected '{title}' but got '{self.driver.find_element(*locator).text}'"
        assert self.driver.find_element(*(By.XPATH,self.POSITION_DEPARTMENT[1].format(department))).is_displayed(), f"Expected '{department}' but got '{self.driver.find_element(*(By.XPATH,self.POSITION_DEPARTMENT[1].format(department))).text}'"
        assert self.driver.find_element(*(By.XPATH,self.POSITION_LOCATION[1].format(position))).is_displayed(), f"Expected '{position}' but got '{self.driver.find_element(*(By.XPATH,self.POSITION_LOCATION[1].format(position))).text}'"
        self.move_to_element(locator)
        self.wait_for_element(self.POSITION_VIEW_DETAILS)
        self.move_to_element(self.POSITION_VIEW_DETAILS)
        assert self.driver.find_element(*self.POSITION_VIEW_DETAILS).is_displayed()

    def open_position(self, title):
        locator = (By.XPATH, self.POSITION_TITLE[1].format(title))
        self.wait_for_element(locator)
        self.move_to_element(locator)
        self.driver.find_element(*self.POSITION_VIEW_DETAILS).click()