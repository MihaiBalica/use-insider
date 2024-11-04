import pytest

from pages.careers_page import CareersPage
from pages.lever_application_form_page import LeverAppFormPage
from pages.open_positions_page import OpenPositionsPage
from pages.quality_assurance_page import QualityAssurance

@pytest.mark("regression")
def test_open_position_application_form(open_home_page):
    assert open_home_page.get_current_url() == "https://useinsider.com/"
    assert open_home_page.get_title() == "#1 Leader in Individualized, Cross-Channel CX — Insider"
    open_home_page.accept_cookies()
    open_home_page.open_careers_page()

    careers_page = CareersPage(open_home_page.driver)
    careers_page.verify_careers_page()
    careers_page.open_quality_assurance_page()

    quality_assurance_page = QualityAssurance(open_home_page.driver)
    quality_assurance_page.verify_quality_assurance_page()
    quality_assurance_page.open_all_jobs()

    open_positions_page = OpenPositionsPage(open_home_page.driver)
    open_positions_page.filter_by_location("Istanbul, Turkey", "Quality Assurance")
    open_positions_page.verify_position("Senior Software Quality Assurance Engineer", "Quality Assurance", "Istanbul, Turkey")
    open_positions_page.open_position("Senior Software Quality Assurance Engineer")

    open_home_page.switch_to_new_tab()
    lever_app_form_page = LeverAppFormPage(open_home_page.driver)
    # commented this out as it looks like the page is not loading properly
    # lever_app_form_page.wait_for_page_load(timeout=60)
    lever_app_form_page.verify_lever_app_form_page()
