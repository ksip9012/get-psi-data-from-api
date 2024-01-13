"""folder_utils モジュールにある関数の test に関するファイル."""
import shutil
import unittest
from pathlib import Path
from sys import path
from typing import Self

from get_psi_data_from_api.modules.folder_utils import (
    create_folder,
    set_folder_paths,
)

test_dir = Path(__file__).resolve().parent

project_root = test_dir.parent
path.insert(0, str(project_root))


class TestFolderUtils(unittest.TestCase):
    """フォルダ関係のモジュールのテストクラス.

    Args:
        unittest
    """

    def setUp(self: Self) -> None:
        """Class 変数の設定.

        Args:
            self (Self):
        """
        self.test_folder = "test_folder"
        self.test_folder_path = create_folder(self.test_folder)

    def tearDown(self: Self) -> None:
        """テスト用のフォルダを削除する.

        Args:
            self (Self):
        """
        shutil.rmtree(self.test_folder, ignore_errors=True)

    def test_create_folder(self: Self) -> str | None:
        """テスト用のフォルダを作成する.

        Args:
            self (Self):

        Raises:
            ValueError: フォルダを作成できなかったときのメッセージ

        Returns:
            str | None:
        """
        new_folder_name = "new_folder"
        new_folder_path = create_folder(new_folder_name)
        existing_folder_path = create_folder(new_folder_name)
        msg = "Do not exist 'new_folder'."
        if existing_folder_path != new_folder_path:
            raise ValueError(msg)

    def test_set_folder_paths(self: Self) -> str | None:
        """Subfolder の存在チェック.

        Args:
            self (Self):

        Raises:
            ValueError: 存在しなかったときのメッセージ

        Returns:
            str | None
        """
        subfolder_path = set_folder_paths("subfolder")
        expected_path = Path.cwd() / "subfolder"
        error_msg = "Sub folder path error."
        if subfolder_path != expected_path:
            raise ValueError(error_msg)

if __name__ == "__main__":
    unittest.main()
