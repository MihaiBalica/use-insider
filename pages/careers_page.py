from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CareersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com/careers/"
        self.CAREERS_PAGE_URL = "https://useinsider.com/careers/"
        self.LOCATIONS_SECTION = (By.XPATH, '//h3[contains(text(),"Our Locations")]')
        self.TEAMS_SECTION = (By.XPATH, '//h3[contains(text(),"Find your calling")]')
        self.LIFE_SECTION = (By.XPATH, '//h2[contains(text(),"Life at Insider")]')
        self.SEE_ALL_TEAMS_BUTTON = (By.XPATH, '//a[text()="See all teams"]')
        self.LINK_TO_QUALITY_ASSURANCE = (By.XPATH, '//a//h3[contains(text(),"Quality Assurance")]')

    def open_careers_page(self):
        self.open_page(self.url)
        return self

    def get_careers_page_title(self):
        return self.get_title()

    def get_careers_page_url(self):
        return self.get_current_url()

    def verify_careers_page(self):
        assert self.get_careers_page_url() == self.CAREERS_PAGE_URL
        assert self.get_element_text(self.LOCATIONS_SECTION) == "Our Locations", f"Expected 'Our Locations' but got '{self.get_element_text(self.LOCATIONS_SECTION)}'"
        assert self.get_element_text(self.TEAMS_SECTION) == "Find your calling", f"Expected 'Find your calling' but got '{self.get_element_text(self.TEAMS_SECTION)}'"
        assert self.get_element_text(self.LIFE_SECTION) == "Life at Insider", f"Expected 'Life at Insider' but got '{self.get_element_text(self.LIFE_SECTION)}'"
        assert self.get_element_text(self.SEE_ALL_TEAMS_BUTTON) == "See all teams", f"Expected 'See all teams' but got '{self.get_element_text(self.SEE_ALL_TEAMS_BUTTON)}'"

    def open_quality_assurance_page(self):
        self.wait_for_element(self.LOCATIONS_SECTION)
        self.move_to_element(self.LOCATIONS_SECTION)
        self.click_element(self.SEE_ALL_TEAMS_BUTTON)
        self.wait_for_element(self.LINK_TO_QUALITY_ASSURANCE)
        self.move_to_element(self.LINK_TO_QUALITY_ASSURANCE)
        self.wait_for_element_to_be_clickable(self.LINK_TO_QUALITY_ASSURANCE)
        self.click_element(self.LINK_TO_QUALITY_ASSURANCE)

