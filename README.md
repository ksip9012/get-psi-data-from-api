# PageSpeed Insights API からのデータ取得

## Repository status

[![Lint with ruff](https://github.com/ksip9012/get-psi-data-from-api/actions/workflows/lint-with-ruff.yml/badge.svg)](https://github.com/ksip9012/get-psi-data-from-api/actions/workflows/lint-with-ruff.yml)
[![CodeQL](https://github.com/ksip9012/get-psi-data-from-api/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ksip9012/get-psi-data-from-api/actions/workflows/github-code-scanning/codeql)

## Dependance

[![mise - version](https://img.shields.io/badge/mise-v2024.2.17-blue.svg)](https://github.com/jdx/mise)
[![Python - version](https://img.shields.io/badge/Python-v3.12.1-blue.svg)](https://www.python.org/)
[![Poetry - version](https://img.shields.io/badge/Poetry-v1.7.1-blue.svg)](https://python-poetry.org/)

| PackageName | Version | Python Version |
| ----------- | ------- | -------------- |
| [requests](https://requests.readthedocs.io/en/latest/) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v2.31.0-blue.svg)](https://pypi.org/project/requests/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.7/3.8/3.9/3.10/3.11-blue.svg) |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v1.0.0-green.svg)](https://pypi.org/project/python-dotenv/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.8/3.9/3.10/3.11/3.12-blue.svg) |
| [pandas](https://pandas.pydata.org/) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v2.2.0-blue.svg)](https://pypi.org/project/pandas/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.9/3.10/3.11/3.12-blue.svg) |
| [ruff](https://docs.astral.sh/ruff/) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v0.1.9-orange.svg)](https://pypi.org/project/ruff/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.7/3.8/3.9/3.10/3.11/3.12-blue.svg) |
| [pytest](https://docs.pytest.org/en/latest/) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v7.4.3-blue.svg)](https://pypi.org/project/pytest/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.8/3.9/3.10/3.11/3.12-blue.svg) |
| [google-cloud-bigquery](https://github.com/googleapis/python-bigquery) | [![PyPI - Version](https://img.shields.io/badge/PyPI-v3.16.0-blue.svg)](https://pypi.org/project/google-cloud-bigquery/) | ![PyPI - Python Version](https://img.shields.io/badge/Python-3.7/3.8/3.9/3.10/3.11/3.12-blue.svg) |

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
  - [ ] unittest じゃなくて pytest を使う
- [ ] GCP 上で利用する場合には BigQuery に出力する機能を追加
    - [ ] cloud functions は 6分以内しか動かないのでそれに収まるように
        - [ ] 1つのurlあたり30秒前後かかるので10個前後に
- [ ] create_value_list 関数に変数が多すぎるのでそこを改善
    - [ ] クラスを導入して変数をまとめる

## PSI の API からデータ取得

- GCP のプロジェクトを作って API キーを作らないと高頻度アクセスができない

```フォルダ構成
get_psi_data_from_api/
│
├── .github/
│   ├── ISSUE_TEMPLATE/        # テンプレートファイルの格納
│   └── workflows/             # GitHub actions の設定ファイル
│
├── .venv/                     # poetry で作った仮想環境
│
├── .vscode/                   # vscode の設定ファイルを入れておく
│   └── settings.json         # vscode の設定ファイル
│
├── data/                      # 計測結果の csv ファイルを格納する
│
├── env/
│   ├── .env                  # 環境変数を入れたファイル
│   └── measurement_urls.csv  # 計測する url を入れたファイル
│
├── get_psi_data_from_api/     # プロジェクトのコードが含まれるフォルダ
│   ├── modules
│   │    ├── __init__.py
│   │    ├── folder_utils.py
│   │    ├── for_getenvs.py
│   │    └── setup_logging.py
│   ├── __init__.py
│   └── main.py
│
├── logs/                      # ログファイルの出力先
│
├── tests/                     # テスト用のフォルダ
│   ├── __init__.py
│   └── test_folder_utils.py
│
├── README.md
├── .gitignore
├── .tool-versions             # mise の管理ファイル
├── poetry.lock                # Poetry のパッケージ・バージョン管理
└── pyproject.toml             # Poetry の設定ファイル
```