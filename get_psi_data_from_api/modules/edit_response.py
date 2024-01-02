import logging

import pandas as pd
from requests import Response

from .setup_logging import get_todays_date


def edit_response(
        response: Response,
        measurement_url: str,
        ) -> pd.DataFrame:
    today: str = get_todays_date().strftime("%Y-%m-%d")
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

    lhr_path = res_json["lighthouseResult"]
    performance = lhr_path["categories"]["performance"]["score"]

    thisurl_values_list = [today, measurement_url, "this url", performance]
    origin_values_list = [today, measurement_url, "origin", performance]
    for metric, value in thisurl_metrics.items():
        if value is not None:
            logging.info(f"This url - {metric}: {value}")
            thisurl_values_list.append(value)
        else:
            logging.info(f"This url - {metric}: Error.")
            thisurl_values_list.append("")
    for metric, value in origin_metrics.items():
        if value is not None:
            logging.info(f"Origin - {metric}: {value}")
            origin_values_list.append(value)
        else:
            logging.info(f"Origin - {metric}: Error.")
            origin_values_list.append("")

    return pd.DataFrame([thisurl_values_list, origin_values_list])


def get_metric_value(json_data, category: str, metric: str):
    try:
        return json_data.get(category, {}).get("metrics", {}).get(metric, {}).get("percentile", {})
    except Exception:
        logging.exception("Json has no value.")
        return None
