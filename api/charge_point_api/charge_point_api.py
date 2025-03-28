from typing import Optional

import allure
from requests import Response

from api.api_client import ApiClient
from config.config_local import SRVC_URL_API
from api.singleton import Singleton


class ChargePointApi(ApiClient, metaclass=Singleton):
    def __init__(self, url=SRVC_URL_API):
        super().__init__(url=url)

    @allure.step("GET charge points")
    def get_point(self, point_id: Optional[str] = None, api_key: Optional[str] = None) -> Response:
        path = "/charge-point"
        params = {"id": point_id}
        return self._get(path=path, params=params, json=None, api_key=api_key)

    @allure.step("CREATE charge point")
    def create_point(self, payload: dict, api_key: Optional[str] = None) -> Response:
        path = "/charge-point"
        return self._post(path=path, json=payload, api_key=api_key)

    @allure.step("DELETE charge point")
    def delete_point(self, charge_point_id: Optional[str] = None, api_key: Optional[str] = None) -> Response:
        path = f"/charge-point/{charge_point_id}"
        return self._delete(path=path, json=None, api_key=api_key)
