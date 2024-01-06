"""フォルダに関連する操作."""
import logging
from pathlib import Path


def set_folder_paths(path:str) -> Path | None:
    """フォルダパスを作成する.

    Args:
        path (str):
            Path オブジェクト または パスの文字列

    Returns:
        Path | None: 作成したフルパス
    """
    try:
        cwd = Path.cwd()
        if path is not None and isinstance(path, str):
            return cwd.joinpath(path)
    except Exception:
        logging.exception("Error getting path: ")
        return None


def create_folder(folder_name: str) -> Path | None:
    """名前を受け取ってフォルダを作成する.

    Args:
        folder_name (str):
            作るフォルダの名前

    Returns:
        Path | None: 作ったフォルダのパス
    """
    try:
        folder_path: Path = Path(folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)
    except Exception:
        logging.exception("Error creating folder: ")
    else:
        return folder_path
