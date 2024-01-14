"""PSI からのデータ取得."""
from datetime import date, datetime, timedelta, timezone
from os import getenv
from sys import stderr

import numpy as np
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from requests import Response, exceptions, get


def main() -> None:
    """PSI の API からデータ取得して csv にする."""
    columns = [
        "date", "locale", "strategy", "url", "this/origin",
        "performance", "accessibility", "best_practices", "seo",
        "cls", "ttfb (ms)", "fcp (ms)", "fid (ms)", "inp (ms)", "lcp (ms)",
    ]
    strategy_list = ["mobile", "desktop"]
    df_result = pd.DataFrame()
    api_url, api_key, dataset_id, table_id = get_envs()
    url_lists = []
    for strategy in strategy_list:
        for measuremet_url in url_lists:
            response = make_api_request(
                api_url, api_key, strategy, measuremet_url,
            )
            if response is not None:
                df_single_page = edit_response(
                    response, strategy, measuremet_url,
                )
                df_result = pd.concat([df_result, df_single_page])
    df_result.columns = columns
    df_result.replace([{}], np.nan)
    resultdata_to_bigquery(df_result, dataset_id, table_id)


def get_envs() -> tuple:
    """環境変数を取得する.

    Returns:
        tuple: 環境変数の塊
    """
    api_url = getenv("API_URL", default="")
    api_key = getenv("API_KEY", default="")
    dataset_id = getenv("DATASET_ID", default="")
    table_id = getenv("TABLE_ID", default="")
    return api_url, api_key, dataset_id, table_id


def get_todays_date() -> date:
    """今日の日付を取得する.

    Returns:
        date: 今日の日付
    """
    tz_jst: timezone = timezone(timedelta(hours=9))
    return datetime.now(tz=tz_jst).date()


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
        api_key (str):
            PSI の API の KEY
        strategy (str):
            mobile / desktop
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
        response = get(api_url, params, timeout=(60, 30))
        response.raise_for_status()
    except exceptions.RequestException as e:
        stderr.write(f"Error on get data from API: {e}")
    else:
        return response


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
    except ValueError as ve:
        stderr.write(f"Json has no value.: {ve}")
        return None


def resultdata_to_bigquery(
        df_result: pd.DataFrame,
        dataset_id: str,
        table_id: str,
        ) -> None:
    """結果のデータを BigQuery に投入する.

    Args:
        df_result (pd.DataFrame):
            結果のデータ
        dataset_id (str):
            BigQuery のデータセット
        table_id (str):
            BigQuery のテーブル
    """
    schema = [
        bigquery.SchemaField(
            name="date",
            field_type="DATE",
            mode="REQUIRED",
        ),
        bigquery.SchemaField(
            name="locale",
            field_type="STRING",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="strategy",
            field_type="STRING",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="url",
            field_type="STRING",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="thisurl_origin",
            field_type="STRING",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="performance",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="accessibility",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="best_practices",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="seo",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="cls",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="ttfb",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="fcp",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="fid",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="inp",
            field_type="INT64",
            mode="NULLABLE",
        ),
        bigquery.SchemaField(
            name="lcp",
            field_type="INT64",
            mode="NULLABLE",
        ),
    ]
    job_config = bigquery.LoadJobConfig(schema=schema)
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True
    job_config.write_disposition = "WRITE_APPEND"
    try:
        load_job = bigquery.Client().load_table_from_dataframe(
            df_result,
            bigquery.Client().dataset(dataset_id).table(table_id),
            job_config=job_config,
        )
        load_job.result()
    except GoogleCloudError as e:
        stderr.write(f"Can't access to BigQuery table: {e}")


if __name__ == "__main__":
    main()
