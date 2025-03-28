import json
from http import HTTPStatus
import allure
from requests import Response

from consts.consts import Colors
from logger.logger import get_logger

logger = get_logger(__name__)


@allure.step("Compare received status code with expected")
def check_status_code(response: Response, expected_status_code: int):
    """
        Compares the response status code with the expected status code.

        :param response: The Response object from a request.
        :param expected_status_code: The expected HTTP status code.
        :raises AssertionError: If the response status code does not match the expected status code.
    """
    expected_code = expected_status_code.value if isinstance(expected_status_code, HTTPStatus) else expected_status_code
    with allure.step(f"Expected status code: {expected_code}"):
        pass
    with allure.step(f"Actual status code: {response.status_code}"):
        pass
    assert response.status_code == expected_status_code, \
            (f"Test failed. HTTP status is : {response.status_code},({response.text}), "
             f"expected  HTTP status: {expected_status_code}")


def pretty_log_request(response: Response, method: str, **kwargs):
    """
        Logs detailed information about an HTTP request and its response.

        :param response: The Response object.
        :param method: HTTP method used for the request.
    """
    logger.info(f"{Colors.GREEN.value}{method} request to {response.url}{Colors.BLACK.value}")

    request_body = kwargs.get("json")
    if request_body is not None:
        json_body = json.dumps(request_body, ensure_ascii=False)
        logger.info(f"{Colors.GREEN.value}Request body is {json_body}{Colors.BLACK.value}")

    logger.info(f"{Colors.GREEN.value}Response status is: {response.status_code}{Colors.BLACK.value}")
    logger.info(f"{Colors.GREEN.value}Response body is {response.text}{Colors.BLACK.value}")


def assert_body(expected: dict, actual: dict, excluded: list = None):
    """
    Compares two dictionaries in nice readable view

    :param expected: Dictionary containing expected key-value pairs
    :param actual: Dictionary containing actual key-value pairs
    :param excluded: List of keys to be excluded from comparison
    :return: None

    """
    excluded = [] if not excluded else excluded
    mismatches = []
    for key, value in expected.items():
        if key in excluded:
            continue
        if actual.get(key) != value:
            mismatches.append(f"{key}: expected {value}, got {actual.get(key)}")

    if mismatches:
        allure.attach("\n".join(mismatches), name="Mismatches", attachment_type=allure.attachment_type.TEXT)
        assert not mismatches, f"Test failed.Different actual body. Mismatches: \n{mismatches}"
