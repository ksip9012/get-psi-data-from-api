"""Logger を設定するモジュール."""
from datetime import date, datetime, timedelta, timezone
from logging import DEBUG, basicConfig, exception

from .folder_utils import create_folder


def setup_logging(
    log_folder: str = "logs",
) -> None:
    """Logger の初期設定.

    Args:
        log_folder (str, optional):
            ログファイルの出力先フォルダ Defaults to "logs".
    """
    log_path = create_folder(log_folder)
    today: date = get_todays_date()
    file_name: str = f"{today}_logfile.log"
    if log_path is not None:
        log_file_path = f"{log_path}/{file_name}"
        basicConfig(
            filename=log_file_path,
            level=DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    else:
        exception("Error logging: ")


def get_todays_date() -> date:
    """今日の日付を取得する.

    Returns:
        date: 今日の日付
    """
    tz_jst: timezone = timezone(timedelta(hours=9))
    return datetime.now(tz=tz_jst).date()
