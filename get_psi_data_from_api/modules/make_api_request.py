"""API への接続に関するモジュール."""
import logging
from time import time

from requests import Response, exceptions, get


def log_request_times(response: Response, start_time: float) -> None:
    """API 接続にかかる時間を計測する.

    Args:
        response (Response):
            API からのレスポンス
        start_time (float):
            API に接続を開始したタイミング
    """
    elapsed_time = time() - start_time
    connect_time = response.elapsed.total_seconds()
    read_time = elapsed_time - connect_time

    logging.info("Connect Time: %s", connect_time)
    logging.info("Read Time: %s", read_time)
    logging.info("Total Time: %s", elapsed_time)


def handle_request_exceptions(e: exceptions.RequestException) -> None:
    """Except の設定.

    Args:
        e (requests.exceptions.RequestException):
            except の返り値
    """
    logging.exception(str(e))


def make_api_request(
        api_url: str,
        api_key: str,
        strategy: str,
        measurement_url: str,
        ) -> Response | None:
    """PSI の API からデータ取得する.

    Args:
        api_url (str):
            PSI の API の URL
        measurement_url (str):
            計測対象の URL

    Returns:
        Response | None: API から取得した内容
    """
    params = {
        "url": measurement_url,
        "locale": "ja",
        "strategy": strategy,
        "key": api_key,
        "category": ["performance", "accessibility", "best-practices", "seo"],
    }
    try:
        start_time = time()
        response = get(api_url, params, timeout=(60, 30))
        response.raise_for_status()
        log_request_times(response, start_time)
        logging.info("Request successful")
    except exceptions.RequestException as e:
        handle_request_exceptions(e)
    else:
        return response
