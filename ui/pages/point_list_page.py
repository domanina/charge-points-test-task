from playwright.sync_api import Page

from config.config_local import SRVC_URL_API
from ui.pages.base_page import BasePage


class ChargePointPage(BasePage):
    URL = SRVC_URL_API

    def __init__(self, page: Page):
        super().__init__(page)

        self.table_label = self.locator("//label[@for='input-serial-number']")
        self.app_title = self.locator("//*[@class='title']")
        self.input_serial_number = self.locator("//input[@name='input-serial-number']")
        self.add_button = self.locator("//button[@class='addButton']")
        self.points_table = self.locator("//ul[@class='list']")
        self.error_alert = self.locator("//ul[@class='error-alert']")
        self.point_serial_number_xpath = "//*[@class='list-text']"
        self.point_delete_button_xpath = "/following-sibling::[@class='list-button']"
