import allure
from assertpy import assert_that

from helpers.common_helper import generate_random_string
from helpers.ui_helper import check_element_visibility
from logger.logger import get_logger

logger = get_logger(__name__)


@allure.step("Add new point")
def add_new_charge_point(page, sn_length: int = 20):
    point_serial_number = generate_random_string(sn_length)
    logger.info(f"Serial number is {point_serial_number}")
    page.input_serial_number.fill(point_serial_number)
    page.add_button.click()
    return point_serial_number


@allure.step("Check existence of point in DB via get request")
def assert_charge_point_in_get_response(charge_point_api_client, point_serial_number: str, should_contain=True):
    response = charge_point_api_client.get_point()
    serial_numbers = [point["serialNumber"] for point in response.json()]
    if should_contain:
        assert_that(serial_numbers, "Point serial number").contains(point_serial_number)
    else:
        assert_that(serial_numbers, "Point serial number").does_not_contain(point_serial_number)


@allure.step("Check existence of point in the table")
def find_point_in_table(page, point_serial_number: str, should_be_visible=True):
    point_in_table = page.points_table.locator(page.point_serial_number_xpath, has_text=point_serial_number)
    check_element_visibility(element=point_in_table, page=page, description="Charge point", should_be_visible=should_be_visible)
    return point_in_table


@allure.step("Delete point from the table")
def delete_point_from_table(page, point_serial_number: str):
    point_locator = page.points_table.locator(page.point_serial_number_xpath, has_text=point_serial_number)
    delete_button = point_locator.locator("xpath=./ancestor::li//button[contains(@class, 'list-button')]")
    delete_button.click()
