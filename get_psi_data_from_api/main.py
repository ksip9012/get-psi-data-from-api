
import pandas as pd
from modules.edit_response import edit_response
from modules.folder_utils import set_folder_paths
from modules.for_getenvs import (
    load_environment_variables,
    load_measurement_urls,
)
from modules.make_api_request import make_api_request
from modules.setup_logging import get_todays_date, setup_logging


def main():
    setup_logging()
    columns = [
        "date", "url", "this/origin", "performance",
        "cls", "ttfb", "fcp", "fid", "inp", "lcp",
    ]
    df_result = pd.DataFrame()
    api_url = load_environment_variables()
    url_lists = load_measurement_urls()
    for measuremet_url in url_lists:
        response = make_api_request(api_url, measuremet_url)
        if response is not None:
            df_single_page = edit_response(response, measuremet_url)
            df_result = pd.concat([df_result, df_single_page])
    df_result.columns = columns
    data_folder_path = set_folder_paths("data/")
    measuremet_date = get_todays_date()
    df_result.to_csv(f"{data_folder_path}/{measuremet_date}_result.csv", index=False)
    print(df_result.reset_index(drop=True))


if __name__ == "__main__":
    main()
