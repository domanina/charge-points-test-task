import allure
from http import HTTPStatus
import pytest
from assertpy import assert_that, soft_assertions

from helpers.api_helper import check_status_code
from helpers.common_helper import generate_random_string, is_valid_uuid4
from logger.logger import get_logger
from models.charge_point import ChargePointModel

logger = get_logger(__name__)


@allure.suite("CREATE charge points")
class TestCreatePoints:

    @allure.title("Create point successfully")
    @pytest.mark.smoke
    def test_create_point(self, charge_point_api_client):
        point_serial_number = generate_random_string()
        charge_point = ChargePointModel(serial_number=point_serial_number)
        response = charge_point_api_client.create_point(payload=charge_point.model_dump(by_alias=True, exclude_none=True))
        with soft_assertions():
            check_status_code(response, HTTPStatus.CREATED)
            assert_that(response.json()["serialNumber"], "Point serial number").is_equal_to(charge_point.serial_number)
            assert_that(is_valid_uuid4(response.json()["id"]), "ID should be valid UUID").is_true()

    @allure.title("Create point with the same serial number - positive case")
    @pytest.mark.smoke
    def test_create_point_same_serial_number(self, charge_point_api_client):
        with allure.step("Create first point"):
            point_serial_number = generate_random_string()
            response = charge_point_api_client.create_point(
                payload=ChargePointModel(serial_number=point_serial_number).model_dump(by_alias=True, exclude_none=True))
            first_charge_point_id = response.json()["id"]
        with allure.step("Create second point with the same serial number - positive case"):
            response = charge_point_api_client.create_point(
                payload=ChargePointModel(serial_number=point_serial_number).model_dump(by_alias=True,exclude_none=True))
            with soft_assertions():
                check_status_code(response, HTTPStatus.CREATED)
                assert_that(response.json()["id"], "Second point serial number").is_not_equal_to(first_charge_point_id)

    @allure.title("Create point with maximum serial number length")
    @pytest.mark.smoke
    def test_create_point_max_sn_length(self, charge_point_api_client):
        point_serial_number = generate_random_string(length=1000)
        charge_point = ChargePointModel(serial_number=point_serial_number)
        response = charge_point_api_client.create_point(
            payload=charge_point.model_dump(by_alias=True, exclude_none=True))
        check_status_code(response, HTTPStatus.CREATED)
        with soft_assertions():
            assert_that(response.json()["serialNumber"], "Point serial number").is_equal_to(charge_point.serial_number)
            assert_that(is_valid_uuid4(response.json()["id"]), "ID should be valid UUID").is_true()

    @allure.title("Create point exceeded maximum serial number length")
    @pytest.mark.negative
    @pytest.mark.skip(reason="POST does not support length validation")
    def test_create_point_max_sn_length_exceeded(self, charge_point_api_client):
        point_serial_number = generate_random_string(length=1001)
        charge_point = ChargePointModel(serial_number=point_serial_number)
        response = charge_point_api_client.create_point(
            payload=charge_point.model_dump(by_alias=True, exclude_none=True))
        with soft_assertions():
            check_status_code(response, HTTPStatus.BAD_REQUEST)
            assert_that(response.json()["message"]).is_equal_to("Max sn length exceeded")

    @allure.title("Create point without body")
    @pytest.mark.negative
    def test_create_point_empty_body(self, charge_point_api_client):
        response = charge_point_api_client.create_point(payload=None)
        with soft_assertions():
            check_status_code(response, HTTPStatus.BAD_REQUEST)
            assert_that(response.json()["message"]).is_equal_to("Missing serial number")

    @allure.title("Create point - not allowed serial number")
    @pytest.mark.negative
    @pytest.mark.parametrize("serial_number", [None, "", " ", "!@$#/"])
    def test_create_point_empty_sn(self, charge_point_api_client, serial_number):
        response = charge_point_api_client.create_point(payload={"serialNumber": serial_number})
        with soft_assertions():
            check_status_code(response, HTTPStatus.BAD_REQUEST)
            assert_that(response.json()["message"]).is_equal_to("invalid serial number")
