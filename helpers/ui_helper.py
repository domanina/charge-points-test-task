import allure
from playwright.sync_api import expect, Page


def make_failure_screenshot(page: Page):
    allure.attach(
        page.screenshot(type="png"),
        name="allure-report/failure",
        attachment_type=allure.attachment_type.PNG)


def check_element_visibility(element, page, description, should_be_visible=True):
    with allure.step(f"Check {description} is {'visible' if should_be_visible else 'not visible'}"):
        if should_be_visible:
            expect(element, make_failure_screenshot(page.page)).to_be_visible()
        else:
            expect(element, make_failure_screenshot(page.page)).not_to_be_visible()


def check_element_text(element, page, description, text, should_contain=True):
    with allure.step(f"Check {description} {'contains' if should_contain else 'does not contain'} text '{text}'"):
        if should_contain:
            expect(element, make_failure_screenshot(page.page)).to_contain_text(text, ignore_case=True)
        else:
            expect(element, make_failure_screenshot(page.page)).not_to_contain_text(text, ignore_case=True)