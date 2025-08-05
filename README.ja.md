> **⚠️ AI 翻訳について / AI Translation Notice**  
> この文書は AI によって英語版から翻訳されました。翻訳の精度については保証できませんので、重要な情報については[英語版](README.md)をご確認ください。  
> _This document has been translated from English by AI. Translation accuracy cannot be guaranteed, so please refer to the [English version](README.md) for critical information._

# フルスタックアプリケーション

Python FastAPI バックエンドを持つモダンなアプリケーションで、Docker でコンテナ化されています。

## 前提条件

- [Docker](https://docs.docker.com/get-docker/) (v20.10 以上)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0 以上)
- [Make](https://www.gnu.org/software/make/) (オプション、便利なコマンド用)

## プロジェクト構造

```
react-fastapi-template/
├── docker-compose.yml          # メインのDocker Compose設定
├── docker-compose.prod.yml     # 本番環境用オーバーライド
├── Makefile                    # 便利なコマンド
├── README.md                   # このファイルの英語版
├── README.ja.md                # このファイル
└── app/                    # Python FastAPIアプリケーション
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── alembic
    │   └── versions            # データベースマイグレーション
    └── src/
        ├── config              # 設定用定数値
        ├── controllers         # ユースケースハンドラー
        ├── dependencies        # 依存性注入
        ├── database            # データベース接続設定
        ├── models              # データベーススキーマモデル定義
        ├── repositories        # データベース操作とクエリ
        ├── routes              # APIルートハンドラー
        ├── services            # 外部サービス
        ├── types               # APIリクエストとレスポンスクラス
        └── utils               # 共通関数
```

## クイックスタート

### 1. クローンとセットアップ

```bash
git clone https://github.com/sodavinchheng/react-fastapi-template.git
cd react-fastapi-template
```

### 2. API キーを追加する

ベースディレクトリに `.env` ファイルを作成します。

```bash
cp .env.sample .env
```

作成された `.env` ファイルに、自分の API キーを追加してください。

### 3. 開発環境の起動

[任意] Python 仮想環境を作成（IDE intellisense 推奨）

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./app/requirements.txt
```

Make を使用（推奨）：

```bash
make dev
```

または Docker Compose を直接使用：

```bash
docker-compose up --build -d
docker-compose exec app alembic upgrade head
```

### 4. アプリケーションへのアクセス

- **REST API**: http://localhost:8000/api
- **API ドキュメント**: （詳細は OpenAPI セクションを参照）
  - _Swagger_: http://localhost:8000/docs
  - _Redoc_: http://localhost:8000/redoc
- **データベース**: localhost:5432 (ユーザー: `user`, パスワード: `password`, DB: `appdb`)

## OpenAPI

FastAPI は自動的に`openapi.json`ファイルを生成し、Swagger UI で表示できます。

## 利用可能なコマンド

Make がインストールされている場合、以下の便利なコマンドを使用できます：

```bash
make dev          # 開発環境の起動
make prod         # 本番環境の起動
make build        # すべてのサービスをビルド
make up           # バックグラウンドでサービスを起動
make down         # すべてのサービスを停止
make restart      # すべてのサービスを再起動
make logs         # すべてのサービスのログを表示
make clean        # コンテナ、イメージ、ボリュームをクリーンアップ

# データベースコマンド
make db-makemigration   # 新しいデータベースマイグレーションを作成
make db-migrate         # データベースマイグレーションを実行
make db-reset           # データベースを初期状態にリセット
```

## 手動 Docker コマンド

Make を使用したくない場合：

```bash
# 開発環境の起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d --build

# サービスの停止
docker-compose down

# ログの表示
docker-compose logs -f

# 特定のサービスの再ビルド
docker-compose build app

# コンテナ内でコマンドを実行
docker-compose exec app python manage.py migrate
```

## 開発ワークフロー

### ホットリロード

バックエンドが開発中のホットリロードをサポートしています：

- FastAPI が`--reload`フラグで Python ファイル変更時に再起動

### 変更の実行

1. `app/`ディレクトリのファイルを編集
2. 変更は実行中のコンテナに自動的に反映
3. データベースの変更は`postgres_data`ボリュームに保持

### 依存関係の追加

**FastAPI（Python）:**

```bash
cd app
pip install <package-name>
echo "<package-name>==<version>" >> requirements.txt
```

その後、コンテナを再ビルド：

```bash
make build
```

## 環境設定

### 開発環境変数

アプリケーションは開発用にこれらのデフォルト環境変数を使用します：

**FastAPI:**

- `DATABASE_URL=postgresql://user:password@db:5432/appdb`
- `CORS_ORIGINS=http://localhost:5173`

**データベース:**

- `POSTGRES_DB=appdb`
- `POSTGRES_USER=user`
- `POSTGRES_PASSWORD=password`

### 本番環境変数

本番環境では、`docker-compose.prod.yml`を以下のように更新してください：

```yaml
environment:
  - DATABASE_URL=postgresql://user:secure_password@db:5432/appdb
  - CORS_ORIGINS=https://yourdomain.com
  - POSTGRES_PASSWORD=your_secure_password_here
```

## 本番デプロイ

### 1. 環境の設定

`docker-compose.prod.yml`を編集して以下を更新：

- ドメイン名
- データベース認証情報
- API URL
- その他の環境固有設定

### 2. デプロイ

```bash
make prod
```

または手動で：

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### 3. 本番機能

- **FastAPI**: パフォーマンス向上のため複数ワーカーで Gunicorn を使用
- **データベース**: 安全な認証情報で永続ストレージ
- **セキュリティ**: 非 root ユーザー、ヘルスチェック、適切な CORS 設定

## データベース管理

### 初期セットアップ

データベースはサービス開始時に自動的に作成されます。初期マイグレーションを実行するには：

```bash
make db-migrate
```

### データベースのリセット

データベースを初期状態にリセットするには：

```bash
make db-reset
```

### 手動データベースアクセス

```bash
docker-compose exec db psql -U user -d appdb
```

## トラブルシューティング

### 一般的な問題

**ポートが既に使用中:**

```bash
# ポートを使用しているサービスを停止
make down
# またはdocker-compose.ymlでポートを変更
```

**データベース接続の問題:**

```bash
# データベースが実行中か確認
docker-compose ps
# データベースログを表示
docker-compose logs db
```

**権限の問題:**

```bash
# クリーンアップと再ビルド
make clean
make build
```

### ログの表示

```bash
# すべてのサービス
make logs

# 特定のサービス
docker-compose logs -f app
docker-compose logs -f db
```

### クリーンアップ

Docker リソースを完全にクリーンアップするには：

```bash
make clean
```

これにより以下が削除されます：

- すべてのコンテナ
- 未使用のイメージ
- 未使用のボリューム
- 未使用のネットワーク

## 開発のヒント

1. **コード変更**: FastAPIがホットリロードをサポート
2. **データベースデータ**: `postgres_data`ボリュームでコンテナ再起動間で保持
3. **ログ**: `make logs`ですべてのサービスを監視
4. **テスト**: `docker-compose exec`でコンテナ内でテストを実行
5. **依存関係**: 新しいパッケージを追加してコンテナを再ビルド

## サポート

問題や質問については：

1. ログを確認: `make logs`
2. Docker が実行中で最新であることを確認
3. クリーンアップと再ビルドを試行: `make clean && make build`
4. Docker Compose 設定ファイルを確認

## ライセンス

MIT
