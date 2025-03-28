import pytest
import allure

from playwright.sync_api import sync_playwright
from api.charge_point_api.charge_point_api import ChargePointApi
from config.config_local import RUN_BROWSER, SRVC_URL_UI
from logger.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def charge_point_api_client():
    api = ChargePointApi()
    yield api


@pytest.fixture(scope="function", autouse=True)
def cleanup_db_before_test():
    # I assume I have access to test bench DB and I can clean up
    # DB will be empty before every single test-run
    # autouse=True means run automatically
    pass


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        if RUN_BROWSER == "webkit":
            browser = playwright.webkit.launch(headless=False)
        elif RUN_BROWSER == "chromium":
            browser = playwright.chromium.launch(headless=False)
        elif RUN_BROWSER == "firefox":
            browser = playwright.firefox.launch(headless=False)
        else:
            raise ValueError(f"Unsupported browser: {RUN_BROWSER}")
        yield browser
        try:
            browser.close()
        except Exception as e:
            logger.error(f"Error while closing browser: {e}")


@pytest.fixture(scope="session")
def new_context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def main_page(new_context):
    page = new_context.new_page()
    with allure.step("Navigate to main app page"):
        page.goto(SRVC_URL_UI)
    yield page
    page.close()
