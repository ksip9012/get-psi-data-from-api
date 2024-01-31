"""結果のデータフレームをcsvファイルとして出力する."""
import pandas as pd

from .folder_utils import set_folder_paths
from .setup_logging import get_todays_date


def resultdata_to_csv(df_result: pd.DataFrame) -> None:
    """結果のデータフレームをcsvファイルとして出力する.

    Args:
        df_result (pd.DataFrame):
            結果のデータフレーム
    """
    output_folder_path = set_folder_paths("data/")
    measurement_date = get_todays_date()
    df_result.to_csv(
        f"{output_folder_path}/{measurement_date}_result.csv",
        index=False,
    )
