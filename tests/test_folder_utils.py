import shutil
import unittest
from pathlib import Path
from sys import path

test_dir = Path(__file__).resolve().parent

project_root = test_dir.parent
path.insert(0, str(project_root))

from get_psi_data_from_api.modules.folder_utils import create_folder, set_folder_paths


class TestFolderUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.test_folder = "test_folder"
        self.test_folder_path = create_folder(self.test_folder)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder, ignore_errors=True)

    def test_create_folder(self):
        new_folder_name = "new_folder"
        new_folder_path = create_folder(new_folder_name)

        self.assertTrue(new_folder_path.exists())

        existing_folder_path = create_folder(new_folder_name)
        self.assertEqual(existing_folder_path, new_folder_path)

    def test_set_folder_paths(self):
        subfolder_path = set_folder_paths("subfolder")

        expected_path = Path.cwd() / "subfolder"
        self.assertEqual(subfolder_path, expected_path)

if __name__ == "__main__":
    unittest.main()
