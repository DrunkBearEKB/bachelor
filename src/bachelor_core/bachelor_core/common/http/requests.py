import decimal
import time
from typing import Optional, Dict, Any
import requests
from http.client import responses

from bachelor_core.application.application import get_application
from bachelor_core.common.http.http_method import HTTPMethod


def http_get(
    url: str,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    hide_request_payload: bool = False,
    hide_response_payload: bool = False,
) -> requests.Response:
    return __http_call(
        url, HTTPMethod.GET, json, headers, hide_request_payload, hide_response_payload
    )


def http_post(
    url: str,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    hide_request_payload: bool = False,
    hide_response_payload: bool = False,
) -> requests.Response:
    return __http_call(
        url, HTTPMethod.POST, json, headers, hide_request_payload, hide_response_payload
    )


def __http_call(
    url: str,
    http_method: str,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    hide_request_payload: bool = False,
    hide_response_payload: bool = False,
) -> requests.Response:
    app = get_application()

    app.log_info(f"sending {http_method} request to {url}")
    if not hide_request_payload:
        app.log_info(f"sending", body=json)
        # app.log_info(f"sending", headers=headers)

    http_func = {
        HTTPMethod.GET: requests.get,
        HTTPMethod.POST: requests.post,
    }[http_method]

    time_started = time.time()
    response: requests.Response = http_func(url=url, json=json, headers=headers)
    time_diff = round(decimal.Decimal(time.time() - time_started), 3)

    app.log_info(
        f"response: {response.status_code} {responses[response.status_code]}",
        body_size=len(response.content),
        query_took=time_diff,
    )

    if not hide_response_payload:
        try:
            app.log_info(
                f"response body: {response.json()}",
            )
        except Exception as e:
            pass

    return response
