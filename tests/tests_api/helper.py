import allure

from helpers.common_helper import generate_random_string
from models.charge_point import ChargePointModel


def create_test_charge_point(charge_point_api_client, serial_number=None):
    point_serial_number = generate_random_string() if not serial_number else serial_number
    with allure.step(f"Create point with serial number={point_serial_number}"):
        charge_point = ChargePointModel(serial_number=point_serial_number)
        response = charge_point_api_client.create_point(payload=charge_point.model_dump(by_alias=True, exclude_none=True))
        charge_point.id = response.json()["id"]
        return charge_point


@allure.step("Find created point in the response list and compare with expected data")
def assert_charge_point_in_list(points_list: list, expected_point: dict, should_exist: bool = True):
    if not points_list and should_exist:
        assert False, "Charge points list is empty but should contain the expected point"

    found = any(all(point.get(key) == value for key, value in expected_point.items())for point in points_list)

    if should_exist and not found:
        assert False, f"Expected charge point not found in the list: {expected_point}"

    if not should_exist and found:
        assert False, f"Charge point should not be in the list, but it was found: {expected_point}"