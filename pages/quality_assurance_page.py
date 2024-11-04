from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class QualityAssurance(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com/careers/quality-assurance/"
        self.QUALITY_ASSURANCE_PAGE_TITLE = "Insider quality assurance job opportunities"
        self.QUALITY_ASSURANCE_PAGE_URL = "https://useinsider.com/careers/quality-assurance/"
        self.QUALITY_ASSURANCE_HEADER = (By.XPATH, '//h1[contains(text(),"Quality Assurance")]')
        self.SEE_ALL_JOBS = (By.XPATH, '//div//a[text()="See all QA jobs"]')

    def verify_quality_assurance_page(self):
        assert self.get_element_text(self.QUALITY_ASSURANCE_HEADER) == "Quality Assurance", f"Expected 'Quality Assurance' but got '{self.get_element_text(self.QUALITY_ASSURANCE_HEADER)}'"
        assert self.get_current_url() == self.QUALITY_ASSURANCE_PAGE_URL, f"Expected '{self.QUALITY_ASSURANCE_PAGE_URL}' but got '{self.get_current_url()}'"
        assert self.get_title() == self.QUALITY_ASSURANCE_PAGE_TITLE, f"Expected '{self.QUALITY_ASSURANCE_PAGE_TITLE}' but got '{self.get_title()}'"

    def open_all_jobs(self):
        self.click_element(self.SEE_ALL_JOBS)
        return self