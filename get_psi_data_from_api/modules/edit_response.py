"""API から取得したデータを整形する."""
import logging

import pandas as pd
from requests import Response

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
        locale: str,
        strategy: str,
        url: str,
        category: str,
        performance: float,
        accessibility: float,
        best_practices: float,
        seo: float,
        metrics: dict,
        ) -> list:
    """結果を list にまとめる.

    Args:
        date (str):
            計測した日付
        locale (str):
            計測する国範囲 (日本に固定中)
        strategy (str):
            mobile / desktop
        url (str):
            計測した url
        category (str):
            thisurl / origin どちらか
        performance (float):
            パフォーマンスの結果
        accessibility (float):
            アクセシビリティの結果
        best_practices (float):
            ベストプラクティスの結果
        seo (float):
            SEO の結果
        metrics (dict):
            PSI の各数値のまとまったもの

    Returns:
        list: 結果をまとめたlist
    """
    values_list = [
        date, locale, strategy, url, category,
        int(performance), int(accessibility), int(best_practices), int(seo),
    ]
    values_list.extend(
        [value if value is not None else "" for value in metrics.values()],
    )
    return values_list


def edit_response(
        response: Response,
        strategy: str,
        measurement_url: str,
        ) -> pd.DataFrame:
    """API から取得した結果から必要な項目を取り出す.

    Args:
        response (Response):
            API からの取得内容
        strategy (str):
            mobile / desktop
        measurement_url (str):
            計測した url

    Returns:
        pd.DataFrame: 結果をまとめたデータフレーム
    """
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
    thisurl_metrics = extract_metrics(
        res_json, "loadingExperience", metrics_list,
    )
    origin_metrics = extract_metrics(
        res_json, "originLoadingExperience", metrics_list,
    )

    cate_path = res_json["lighthouseResult"]["categories"]
    performance = cate_path["performance"]["score"] * 100
    accessibility = cate_path["accessibility"]["score"] * 100
    best_practices = cate_path["best-practices"]["score"] * 100
    seo = cate_path["seo"]["score"] * 100

    thisurl_values_list = create_value_list(
        today, "ja", strategy, measurement_url, "this url",
        performance, accessibility, best_practices, seo, thisurl_metrics,
    )
    origin_values_list = create_value_list(
        today, "ja", strategy, measurement_url, "origin",
        performance, accessibility, best_practices, seo, origin_metrics,
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
