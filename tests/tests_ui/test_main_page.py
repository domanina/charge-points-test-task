import allure
import pytest
from assertpy import assert_that

from helpers.ui_helper import check_element_visibility, check_element_text
from logger.logger import get_logger
from tests.tests_ui.helper import add_new_charge_point, assert_charge_point_in_get_response, find_point_in_table, \
    delete_point_from_table


logger = get_logger(__name__)


@allure.label("UI")
@allure.story("Main page")
class TestMainPageUI:

    @allure.title("App title visibility")
    @pytest.mark.smoke
    def test_logo_visibility(self, charge_point_page):
        check_element_visibility(element=charge_point_page.app_title, page=charge_point_page, description="App logo")
        check_element_text(element=charge_point_page.app_title, page=charge_point_page, text="Charge Point Installation Form", description="App title text")

    @allure.title("Table label visibility")
    @pytest.mark.smoke
    def test_table_label_visibility(self, charge_point_page):
        check_element_visibility(element=charge_point_page.table_label, page=charge_point_page, description="Table logo")
        check_element_text(element=charge_point_page.app_title, page=charge_point_page, text="Serial Number:", description="App title text")

    @allure.title("SN Input and and button visibility")
    @pytest.mark.smoke
    def test_input_add_button_visibility(self, main_page):
        check_element_visibility(element=charge_point_page.input_serial_number, page=charge_point_page, description="SN input")
        check_element_visibility(element=charge_point_page.add_button, page=charge_point_page, description="Add button")

    @allure.title("Add new charge point")
    @pytest.mark.smoke
    def test_add_new_charge_point(self, charge_point_page, charge_point_api_client):
        point_serial_number = add_new_charge_point(charge_point_page)
        find_point_in_table(page=charge_point_page, point_serial_number=point_serial_number)
        assert_charge_point_in_get_response(charge_point_api_client, point_serial_number=point_serial_number)

    @allure.title("Add few charge points")
    @pytest.mark.smoke
    def test_add_few_charge_points(self, charge_point_page, charge_point_api_client):
        created_sns = []
        for i in range(10):
            point_serial_number = add_new_charge_point(charge_point_page)
            created_sns.append(point_serial_number)
            find_point_in_table(page=charge_point_page, point_serial_number=point_serial_number)
            assert_charge_point_in_get_response(charge_point_api_client, point_serial_number=point_serial_number)
        with allure.step("Make sure all new points in the table"):
            points_in_table = charge_point_page.points_table.locator(charge_point_page.point_serial_number_xpath)
            assert_that(points_in_table.count()).is_equal_to(9)

    @allure.title("Add new charge point with max length")
    def test_add_new_charge_point_max_length(self, charge_point_page, charge_point_api_client):
        point_serial_number = add_new_charge_point(charge_point_page, sn_length=1000)
        find_point_in_table(charge_point_page, point_serial_number=point_serial_number)
        assert_charge_point_in_get_response(charge_point_api_client, point_serial_number=point_serial_number)

    @allure.title("Add new charge point with max length exceeded")
    def test_add_new_charge_point_max_length_exceeded(self, charge_point_page, charge_point_api_client):
        add_new_charge_point(charge_point_page, sn_length=1001)
        check_element_visibility(element=charge_point_page.error_alert, page=charge_point_page, description="error alert")

    @allure.title("Delete just created point")
    @pytest.mark.smoke
    def test_delete_charge_point(self, charge_point_page, charge_point_api_client):
        point_serial_number = add_new_charge_point(charge_point_page)
        delete_point_from_table(charge_point_page, point_serial_number=point_serial_number)
        find_point_in_table(charge_point_page,point_serial_number= point_serial_number, should_be_visible=False)
        assert_charge_point_in_get_response(charge_point_api_client, point_serial_number=point_serial_number, should_contain=False)
