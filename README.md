# プロジェクト内容

## 概要

- PageSpeed Insights API と Python を利用して計測した結果を取得する
    - env フォルダ内の measurement_urls.csv に計測したいページを置く
    - origin と this url の両方を取得する
    - 結果も csv ファイルで取得する
    - mobile / desktop 両方計測
    - 1url あたり計測に 30 秒前後
- Linter は ruff

## Todo

- [x] 複数 url に対して連続して計測できるような機能追加
    - [x] PSI の api key を利用する機能追加
    - [x] 連続計測する機能
    - [x] ひとつのデータフレームにまとめる機能
- [x] 結果を csv ファイルなどに出力する機能を追加
- [ ] テストコードをちゃんと書く
- [ ] GCP 上で利用する場合には BigQuery に出力する機能を追加
    - [ ] cloud functions は 6分以内しか動かないのでそれに収まるように
        - [ ] 1つのurlあたり30秒前後かかるので10個前後に
- [ ] create_value_list 関数に変数が多すぎるのでそこを改善

## Requirements

- python: 3.12
- requests: 2.31.0
- python-dotenv: 1.0.0
- pathlib: 1.0.1
- pandas: 2.1.4

## PSI の API からデータ取得

- GCP のプロジェクトを作って API キーを作らないと高頻度アクセスができない

```フォルダ構成
get_psi_data_from_api/
│
├── .venv/  # poetry で作った仮想環境
│
├── .vscode/  # vscode の設定ファイルを入れておく
│   └── settings.json # vscode の設定ファイル
│
├── data/  # 計測結果の csv ファイルを格納する
│
├── docs/  # ドキュメンテーション用のフォルダ
│   ├── conf.py
│   ├── index.rst
│   └── ...
│
├── env/  # 環境変数等に関するファイルを格納する
│   ├── .env # 環境変数を入れたファイル
│   └── measurement_urls.csv # 計測する url を入れたファイル
│
├── get_psi_data_from_api/  # プロジェクトのコードが含まれるフォルダ
│   ├── modules
│   │    ├── __init__.py
│   │    ├── folder_utils.py
│   │    ├── for_getenvs.py
│   │    └── setup_logging.py
│   ├── __init__.py
│   └── main.py
│
├── logs/  # ログファイルの出力先
│
├── tests/  # テスト用のフォルダ
│   ├── __init__.py
│   └── test_folder_utils.py
│
├── README.md  # このドキュメント
├── .gitignore  # git が無視するファイルやディレクトリを指定
├── .tool-versions  # rtx の管理ファイル
├── poetry.lock  # Poetry のパッケージ・バージョン管理
└── pyproject.toml  # Poetry の設定ファイル
```
