# プロジェクト内容

## Todo

- [ ] 複数 url に対して連続して計測できるような機能追加
  - [ ] PSI の api key を利用する機能追加
  - [x] 連続計測する機能
  - [x] ひとつのデータフレームにまとめる機能
- [ ] 結果を csv ファイルなどに出力する機能を追加
  - [x] 出力するだけの機能
  - [ ] インデックスの番号を消す機能
  - [ ] 数値がない際に入っている{}を消す機能
  - [ ] 関数として分割
- [ ] GCP 上で利用する場合には BigQuery に出力する機能を追加
    - [ ] cloud functions は 6分以内しか動かないのでそれに収まるように
      - [ ] 1つのurlあたり30秒前後かかるので10個前後に

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

## APIからの返答に含まれるデータ

```
loadingExperience:
    エンドユーザーのページ読み込みエクスペリエンスの指標です。
    これは、特定のページに対するユーザーの体験を表します。
originLoadingExperience:
    オリジンの集約されたページ読み込みエクスペリエンスのメトリックです。
    これは、特定のドメイン全体におけるユーザーの体験を表します。
lighthouseResult:
    監査URLに対するLighthouseの応答をオブジェクトとして表します。
    これは、特定のページのパフォーマンス、アクセシビリティ、SEOなどの詳細な分析結果を提供します。
```