from bachelor_core.common.http.requests import http_post
from bachelor_core.application.plugins.secrets import get_value_from_secrets


def get_iam_token() -> str:
    """
    https://cloud.yandex.ru/docs/iam/operations/iam-token/create-for-sa

    Returns:
        str - IAM-токен
    """
    try:
        yandex_passport_oauth_token = get_value_from_secrets("yandexPassportOauthToken")
        resp = http_post(
            "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            json={
                "yandexPassportOauthToken": yandex_passport_oauth_token,
            },
            hide_request_payload=True,
            hide_response_payload=True,
        )
        return resp.json().get("iamToken")
    except Exception:
        return None
