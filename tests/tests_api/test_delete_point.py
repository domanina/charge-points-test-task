import allure
from http import HTTPStatus
import pytest
from assertpy import assert_that

from helpers.api_helper import check_status_code
from helpers.common_helper import generate_random_string, generate_uuid4
from logger.logger import get_logger
from tests.tests_api.helper import assert_charge_point_in_list, create_test_charge_point

logger = get_logger(__name__)


@allure.suite("DELETE charge points")
class TestDeletePoints:

    @allure.title("Delete just created charge point")
    @pytest.mark.smoke
    def test_delete_just_created_charge_point(self, charge_point_api_client):
        with allure.step("Create point"):
            charge_point = create_test_charge_point(charge_point_api_client)
        with allure.step("Successfully delete point"):
            response = charge_point_api_client.delete_point(charge_point_id=charge_point.id)
            check_status_code(response, HTTPStatus.NO_CONTENT)
        with allure.step("Via get request make sure point is deleted"):
            response = charge_point_api_client.get_point()
            check_status_code(response, HTTPStatus.OK)
            assert_charge_point_in_list(points_list=response.json(),
                                        expected_point=charge_point.model_dump(by_alias=True, exclude_none=True),
                                        should_exist=False
                                        )

    @allure.title("Delete point with the same serial number")
    @pytest.mark.smoke
    def test_delete_point_with_same_sn(self, charge_point_api_client):
        with allure.step("Create 2 points with the same serial number"):
            point_serial_number = generate_random_string()
            first_point = create_test_charge_point(charge_point_api_client, serial_number=point_serial_number)
            second_point = create_test_charge_point(charge_point_api_client, serial_number=point_serial_number)
        with allure.step("Successfully delete first point"):
            response = charge_point_api_client.delete_point(charge_point_id=first_point.id)
            check_status_code(response, HTTPStatus.NO_CONTENT)
        with allure.step("Via get request make sure first point is deleted, second point is in the list"):
            response = charge_point_api_client.get_point()
            check_status_code(response, HTTPStatus.OK)
            assert_charge_point_in_list(points_list=response.json(),
                                        expected_point=first_point.model_dump(by_alias=True, exclude_none=True),
                                        should_exist=False
                                        )
            assert_charge_point_in_list(points_list=response.json(),
                                        expected_point=second_point.model_dump(by_alias=True, exclude_none=True),
                                        )

    @allure.title("Delete deleted charge point")
    def test_delete_deleted_charge_point(self, charge_point_api_client):
        with allure.step("Create point and delete it"):
            charge_point = create_test_charge_point(charge_point_api_client)
            charge_point_api_client.delete_point(charge_point_id=charge_point.id)
        with allure.step("Delete deleted point"):
            response = charge_point_api_client.delete_point(charge_point_id=charge_point.id)
            check_status_code(response, HTTPStatus.NOT_FOUND)
            assert_that(response.json()["message"]).is_equal_to("point not found")

    @allure.title("Delete not exist charge point")
    def test_delete_not_exist_charge_point(self, charge_point_api_client):
        response = charge_point_api_client.delete_point(charge_point_id=generate_uuid4())
        check_status_code(response, HTTPStatus.NOT_FOUND)
        assert_that(response.json()["message"]).is_equal_to("point not found")

    @allure.title("Delete charge point with not correct ID")
    @pytest.mark.negative
    def test_delete_charge_point_not_correct_id(self, charge_point_api_client):
        response = charge_point_api_client.delete_point(charge_point_id=generate_random_string())
        check_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_that(response.json()["message"]).is_equal_to("invalid id format")

    @allure.title("Delete charge point without ID")
    @pytest.mark.negative
    def test_delete_charge_point_without_id(self, charge_point_api_client):
        response = charge_point_api_client.delete_point()
        check_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_that(response.json()["message"]).is_equal_to("invalid id format")
