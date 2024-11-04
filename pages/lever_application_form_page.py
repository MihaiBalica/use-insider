from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LeverAppFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://jobs.lever.co/useinsider/"
        self.APPLY_FOR_THIS_JOB = (By.XPATH, '//a[text()="Apply for this job"]')

    def verify_lever_app_form_page(self):
        assert str(self.get_current_url()).startswith(self.url), \
            f"Expected '{self.url}' but got '{self.get_current_url()}'"
        assert self.get_element_text(self.APPLY_FOR_THIS_JOB) == "Apply for this job", \
            f"Expected 'Apply for this job' but got '{self.get_element_text(self.APPLY_FOR_THIS_JOB)}'"
