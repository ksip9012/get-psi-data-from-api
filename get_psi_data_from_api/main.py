"""PSI からのデータ取得."""
import numpy as np
import pandas as pd
from modules.edit_response import edit_response
from modules.folder_utils import set_folder_paths
from modules.for_getenvs import (
    load_environment_variables,
    load_measurement_urls,
)
from modules.make_api_request import make_api_request
from modules.setup_logging import get_todays_date, setup_logging


def main() -> None:
    """PSI の API からデータ取得して csv にする."""
    setup_logging()
    columns = [
        "date", "locale", "strategy", "url", "this/origin",
        "performance", "accessibility", "best_practices", "seo",
        "cls", "ttfb (ms)", "fcp (ms)", "fid (ms)", "inp (ms)", "lcp (ms)",
    ]
    strategy_list = ["mobile", "desktop"]
    df_result = pd.DataFrame()
    api_url, api_key = load_environment_variables()
    url_lists = load_measurement_urls()
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
    data_folder_path = set_folder_paths("data/")
    measuremet_date = get_todays_date()
    df_result.to_csv(
        f"{data_folder_path}/{measuremet_date}_result.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
