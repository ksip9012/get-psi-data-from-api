from pathlib import Path

import pandas as pd
from modules.edit_response import edit_response
from modules.for_getenvs import (
    load_environment_variables,
    load_measurement_urls,
)
from modules.make_api_request import make_api_request
from modules.setup_logging import setup_logging


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
    cd_base = Path.cwd()
    data_folder_path = cd_base.joinpath("data/")
    df_result.to_csv(f"{data_folder_path}/result.csv")
    print(df_result.reset_index(drop=True))


if __name__ == "__main__":
    main()
