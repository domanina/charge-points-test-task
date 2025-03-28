import allure
from http import HTTPStatus
import pytest
from assertpy import assert_that

from helpers.api_helper import check_status_code
from logger.logger import get_logger
from tests.tests_api.helper import assert_charge_point_in_list, create_test_charge_point

logger = get_logger(__name__)


@allure.suite("GET charge points")
class TestGetPoints:

    @allure.title("Get just created charge point")
    @pytest.mark.smoke
    def test_get_just_created_charge_point(self, charge_point_api_client):
        charge_point = create_test_charge_point(charge_point_api_client)
        response = charge_point_api_client.get_point()
        check_status_code(response, HTTPStatus.OK)
        assert_charge_point_in_list(points_list=response.json(), expected_point=charge_point.model_dump(by_alias=True, exclude_none=True))

    @allure.title("Get few points")
    @pytest.mark.smoke
    def test_get_few_charge_points(self, charge_point_api_client):
        first_charge_point = create_test_charge_point(charge_point_api_client)
        second_charge_point = create_test_charge_point(charge_point_api_client)
        response = charge_point_api_client.get_point()
        check_status_code(response, HTTPStatus.OK)
        assert_that(len(response.json()), "response list length").is_equal_to(2)
        assert_charge_point_in_list(points_list=response.json(),
                                    expected_point=first_charge_point.model_dump(by_alias=True, exclude_none=True))
        assert_charge_point_in_list(points_list=response.json(),
                                    expected_point=second_charge_point.model_dump(by_alias=True, exclude_none=True))

    @allure.title("Get empty points list")
    @pytest.mark.smoke
    def test_get_empty_point_list(self, charge_point_api_client):
        response = charge_point_api_client.get_point()
        check_status_code(response, HTTPStatus.OK)
        assert_that(response.json(), "Empty point list").is_equal_to([])

    @allure.title("Get deleted point")
    def test_get_deleted_point(self, charge_point_api_client):
        with allure.step("Create point and delete it"):
            charge_point = create_test_charge_point(charge_point_api_client)
            charge_point_api_client.delete_point(charge_point_id=charge_point.id)

        with allure.step("Make sure point is not in the list"):
            response = charge_point_api_client.get_point()
            check_status_code(response, HTTPStatus.OK)
            assert_charge_point_in_list(points_list=response.json(),
                                        expected_point=charge_point.model_dump(by_alias=True, exclude_none=True),
                                        should_exist=False
                                        )

    @allure.title("Get not exist point")
    @pytest.mark.negative
    @pytest.mark.skip(reason="GET endpoint does not support query params like id")
    def test_get_not_exist_point(self, charge_point_api_client):
        response = charge_point_api_client.get_point(point_id="not_exist")
        check_status_code(response, HTTPStatus.NOT_FOUND)
        assert_that(response.json()["message"]).is_equal_to("point not found")

    @allure.title("Get point with not allowed id")
    @pytest.mark.negative
    @pytest.mark.skip(reason="GET endpoint does not support type validation")
    @pytest.mark.parametrize("point_id", [None, "!@$#/", " ", "3,4", "3.4"])
    def test_get_point_wrong_id(self, charge_point_api_client, point_id):
        response = charge_point_api_client.get_point(point_id=point_id)
        check_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_that(response.json()["message"]).is_equal_to("invalid id format")
