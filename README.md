# READ ME
## これはもんちゃんブランチ

## プロジェクト開始時の手順

1. 必要パッケージのインストール

   1-1. GitHub からクローンしてきた後、そのフォルダに移動して、以下のコマンドをシェルで実行する。

   1-2. 仮想環境の Python やパッケージが置かれるフォルダ (.venv) がプロジェクトフォルダ内に生成される様に設定します

   `poetry config virtualenvs.in-project true`

   1-3. 必要パッケージのインストール

   `poetry install`

   1-4. 仮想環境に入る

   `poetry shell`

1. pre-commit の導入

   以下のコマンドを実行

   `pre-commit install --hook-type pre-commit --hook-type pre-push`

1. マイグレーションを実行して、データベースにテーブルの作成。
   f
   `python manage.py migrate`

1. .env ファイルの用意

   機密情報のため GitHub には上げられない値は、プロジェクトフォルダ直下に `.env` というファイルを配置し、それに記述する 。

## その他

### VSCode 拡張機能

以下の拡張機能をVSCodeにインストールする。

- Ruff (<https://github.com/astral-sh/ruff>)
- EditorConfig for VS Code
- Code Spell Checker
