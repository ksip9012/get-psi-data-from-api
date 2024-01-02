import logging
from time import time

import requests
from modules.for_getenvs import load_environment_variables, load_measurement_urls
from modules.setup_logging import setup_logging


def make_api_request(
        api_url: str,
        measurement_url: str,
        ):
    params = {
        "url": measurement_url,
        "locale": "ja",
        "strategy": "mobile",
    }
    try:
        start_time = time()
        response = requests.get(api_url, params, timeout=(60, 30))
        end_time = time()

        response.raise_for_status()

        # 接続時間と読み取り時間の計算
        elapsed_time = end_time - start_time
        connect_time = response.elapsed.total_seconds()
        read_time = elapsed_time - connect_time

        logging.info("Connect Time: %s", connect_time)
        logging.info("Read Time: %s", read_time)
        logging.info("Total Time: %s", elapsed_time)
        logging.info("Request successful")

    except requests.exceptions.Timeout:
        logging.exception("Request timed out")
    except requests.exceptions.HTTPError:
        logging.exception("HTTP Error:")
    except requests.exceptions.ConnectionError:
        logging.exception("Error Connecting:")
    except requests.exceptions.RequestException:
        logging.exception("Request error:")
    else:
        return response


def edit_response(response):
    res_json = response.json()
    metrics_list = [
        "CUMULATIVE_LAYOUT_SHIFT_SCORE",
        "EXPERIMENTAL_TIME_TO_FIRST_BYTE",
        "FIRST_CONTENTFUL_PAINT_MS",
        "FIRST_INPUT_DELAY_MS",
        "INTERACTION_TO_NEXT_PAINT",
        "LARGEST_CONTENTFUL_PAINT_MS",
    ]
    thisurl_metrics = {
        metric: get_metric_value(res_json, "loadingExperience", metric)
        for metric in metrics_list
    }
    origin_metrics = {
        metric: get_metric_value(res_json, "originLoadingExperience", metric)
        for metric in metrics_list
    }

    for metric, value in thisurl_metrics.items():
        if value is not None:
            print(f"This url - {metric}: {value}")
        else:
            print(f"This url - {metric}: Error.")
    for metric, value in origin_metrics.items():
        if value is not None:
            print(f"Origin - {metric}: {value}")
        else:
            print(f"Origin - {metric}: Error.")

    lhr_path = res_json["lighthouseResult"]
    print(f"パフォーマンス: {lhr_path["categories"]['performance']['score']}")


def get_metric_value(json_data, category: str, metric: str):
    try:
        return json_data[category]["metrics"][metric]["percentile"]
    except KeyError:
        logging.exception("KeyError: ")
        return None
    except TypeError:
        logging.exception("TypeError: ")
        return None


def main():
    setup_logging()
    api_url = load_environment_variables()
    url_lists = load_measurement_urls()
    for measuremet_url in url_lists:
        response = make_api_request(api_url, measuremet_url)
        edit_response(response)


if __name__ == "__main__":
    main()
