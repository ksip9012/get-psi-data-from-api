"""変数取得関係."""
from os import getenv

from dotenv import load_dotenv

from .folder_utils import set_folder_paths


def load_environment_variables() -> tuple:
    """設定変数をenvファイルから取得する.

    Returns:
        tuple: 変数色々
    """
    envfile_path = set_folder_paths(path="env/.env")
    load_dotenv(envfile_path)
    api_url = getenv("API_URL", default="")
    measurement_url = getenv("MEASUREMENT_URL", default="")
    return api_url, measurement_url
