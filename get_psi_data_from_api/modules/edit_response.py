"""API から取得したデータを整形する."""
import json
import logging
from pathlib import Path

import pandas as pd
from requests import Response

from .folder_utils import set_folder_paths
from .setup_logging import get_todays_date


def extract_metrics(
        json_data: dict,
        category: str,
        metrics_list: list,
        ) -> dict:
    """API から取得したデータから項目を取り出す.

    Args:
        json_data (dict):
            API からの結果を json 化したもの
        category (str):
            thisurl / origin どっちか
        metrics_list (list):
            取り出す項目の名前のリスト

    Returns:
        dict: 結果の数値をまとめたもの
    """
    return {
        metric: get_metric_value(json_data, category, metric)
        for metric in metrics_list
    }


def create_value_list(
        date: str,
        url: str,
        category: str,
        performance: float,
        metrics: dict,
        ) -> list:
    """結果を list にまとめる.

    Args:
        date (str):
            計測した日付
        url (str):
            計測した url
        category (str):
            thisurl / origin どちらか
        performance (float):
            パフォーマンスの結果
        metrics (dict):
            PSI の各数値のまとまったもの

    Returns:
        list: 結果をまとめたlist
    """
    values_list = [date, url, category, performance]
    values_list.extend(
        [value if value is not None else "" for value in metrics.values()],
    )
    return values_list


def edit_response(
        response: Response,
        measurement_url: str,
        ) -> pd.DataFrame:
    """API から取得した結果から必要な項目を取り出す.

    Args:
        response (Response):
            API からの取得内容
        measurement_url (str):
            計測した url

    Returns:
        pd.DataFrame: 結果をまとめたデータフレーム
    """
    today: str = get_todays_date().strftime("%Y-%m-%d")
    res_json = response.json()
    with Path.open(Path(f"{set_folder_paths('data/')}/full.json"), "w") as f:
        json.dump(res_json, f)
    metrics_list = [
        "CUMULATIVE_LAYOUT_SHIFT_SCORE",
        "EXPERIMENTAL_TIME_TO_FIRST_BYTE",
        "FIRST_CONTENTFUL_PAINT_MS",
        "FIRST_INPUT_DELAY_MS",
        "INTERACTION_TO_NEXT_PAINT",
        "LARGEST_CONTENTFUL_PAINT_MS",
    ]
    thisurl_metrics = extract_metrics(
        res_json, "loadingExperience", metrics_list,
    )
    origin_metrics = extract_metrics(
        res_json, "originLoadingExperience", metrics_list,
    )

    lhr_path = res_json["lighthouseResult"]
    performance = lhr_path["categories"]["performance"]["score"]

    thisurl_values_list = create_value_list(
        today, measurement_url, "this url", performance, thisurl_metrics,
    )
    origin_values_list = create_value_list(
        today, measurement_url, "origin", performance, origin_metrics,
    )

    return pd.DataFrame([thisurl_values_list, origin_values_list])


def get_metric_value(
        json_data: dict,
        category: str,
        metric: str,
        ) -> str | None:
    """結果のjsonから項目を抜き出す.

    Args:
        json_data (dict):
            API から取得した丸ごとデータ
        category (str):
            絞り込みに使う結果のカテゴリ
        metric (str):
            取得する項目

    Returns:
        dict | None: 取得した項目
    """
    try:
        return json_data.get(category, {}) \
                        .get("metrics", {}) \
                        .get(metric, {}) \
                        .get("percentile", {})
    except Exception:
        logging.exception("Json has no value.")
        return None
