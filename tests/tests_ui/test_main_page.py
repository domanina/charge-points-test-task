import allure
import pytest
from assertpy import assert_that

from helpers.ui_helper import check_element_visibility, check_element_text
from logger.logger import get_logger
from tests_ui.helper import add_new_charge_point, find_point_get_request, find_point_in_table, delete_point_from_table
from ui.pages.point_list_page import ChargePointPage

logger = get_logger(__name__)


@allure.label("UI")
@allure.story("Main page")
class TestMainPageUI:

    @allure.title("App title visibility")
    @pytest.mark.smoke
    def test_logo_visibility(self, main_page):
        page = ChargePointPage(main_page)
        check_element_visibility(element=page.app_title, page=page, description="App logo")
        check_element_text(element=page.app_title, page=page, text="Charge Point Installation Form", description="App title text")

    @allure.title("Table label visibility")
    @pytest.mark.smoke
    def test_table_label_visibility(self, main_page):
        page = ChargePointPage(main_page)
        check_element_visibility(element=page.table_label, page=page, description="Table logo")
        check_element_text(element=page.app_title, page=page, text="Serial Number:", description="App title text")

    @allure.title("SN Input and and button visibility")
    @pytest.mark.smoke
    def test_input_add_button_visibility(self, main_page):
        page = ChargePointPage(main_page)
        check_element_visibility(element=page.input_serial_number, page=page, description="SN input")
        check_element_visibility(element=page.add_button, page=page, description="Add button")

    @allure.title("Add new charge point")
    @pytest.mark.smoke
    def test_add_new_charge_point(self, main_page, charge_point_api_client):
        page = ChargePointPage(main_page)
        point_serial_number = add_new_charge_point(page)
        find_point_in_table(page=page, point_serial_number=point_serial_number)
        find_point_get_request(charge_point_api_client, point_serial_number=point_serial_number)

    @allure.title("Add few charge points")
    @pytest.mark.smoke
    def test_add_few_charge_points(self, main_page, charge_point_api_client):
        page = ChargePointPage(main_page)
        created_sns = []
        for i in range(10):
            point_serial_number = add_new_charge_point(page)
            created_sns.append(point_serial_number)
            find_point_in_table(page=page, point_serial_number=point_serial_number)
            find_point_get_request(charge_point_api_client, point_serial_number=point_serial_number)
        with allure.step("Make sure all new points in the table"):
            points_in_table = page.points_table.locator(page.point_serial_number_xpath)
            assert_that(points_in_table.count()).is_equal_to(9)

    @allure.title("Add new charge point with max length")
    def test_add_new_charge_point_max_length(self, main_page, charge_point_api_client):
        page = ChargePointPage(main_page)
        point_serial_number = add_new_charge_point(page, sn_length=1000)
        find_point_in_table(page, point_serial_number=point_serial_number)
        find_point_get_request(charge_point_api_client, point_serial_number=point_serial_number)

    @allure.title("Add new charge point with max length exceeded")
    def test_add_new_charge_point_max_length_exceeded(self, main_page, charge_point_api_client):
        page = ChargePointPage(main_page)
        add_new_charge_point(page, sn_length=1001)
        check_element_visibility(element=page.error_alert, page=page, description="error alert")

    @allure.title("Delete just created point")
    @pytest.mark.smoke
    def test_delete_charge_point(self, main_page, charge_point_api_client):
        page = ChargePointPage(main_page)
        point_serial_number = add_new_charge_point(page)
        delete_point_from_table(page, point_serial_number=point_serial_number)
        find_point_in_table(page,point_serial_number= point_serial_number, should_be_visible=False)
        find_point_get_request(charge_point_api_client, point_serial_number=point_serial_number, should_contain=False)
