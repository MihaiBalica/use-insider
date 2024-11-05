from webbrowser import Chrome

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.home_page import HomePage

@pytest.fixture(scope='session')
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless=new")

    selenium_grid_url = "http://selenium-hub-service:4444/wd/hub"
    ChromeDriverManager().install()
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Remote(command_executor=selenium_grid_url, options=options)
    driver.implicitly_wait(30)
    driver.maximize_window()

    yield driver
    driver.quit()

@pytest.fixture(scope='function')
def open_home_page(browser):
    home_page = HomePage(browser)
    home_page.open_home_page()
    return home_page