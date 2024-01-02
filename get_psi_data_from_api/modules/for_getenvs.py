"""変数取得関係."""
import logging
from os import getenv

import pandas as pd
from dotenv import load_dotenv

from .folder_utils import set_folder_paths


def load_environment_variables() -> str:
    """設定変数をenvファイルから取得する.

    Returns:
        tuple: 変数色々
    """
    envfile_path = set_folder_paths(path="env/.env")
    load_dotenv(envfile_path)
    return getenv("API_URL", default="")



def load_measurement_urls() -> list:
    """計測する url のリストを csv ファイルから取得する.

    Returns:
        list: 計測する url のリスト
    """
    csvfile_path = set_folder_paths(path="env/measurement_urls.csv")
    if csvfile_path is not None:
        try:
            df_urls = pd.read_csv(csvfile_path)
            return df_urls["measurement_url"].tolist()
        except Exception:
            logging.exception("Error loading measurement URLs:")
            return []
    else:
        logging.exception("Error: csvfile_path is None.")
        return []
