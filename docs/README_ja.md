# FitScheduler

スポーツコーチと施設予約管理のためのバックエンドAPIサービス。

## プロジェクト概要

FitSchedulerは、スポーツコーチや施設予約のために設計された多機能予約管理システムです。システムは以下をサポートしています：

- ユーザー、コーチ、施設の管理
- 予約の作成と管理
- 支払い方法の管理
- 評価とお気に入り機能
- 認証と認可
- 異なるユーザーロールの権限管理

## インストールガイド

### 要件

- Python 3.8+
- MySQL 5.7+
- Node.js 16+ (フロントエンド部分)

### インストール手順

1. リポジトリをクローン：

```bash
git clone https://github.com/yourusername/bsweetOrder-yoyaku.git
cd bsweetOrder-yoyaku
```

2. 仮想環境を作成し、有効化：

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 依存関係のインストール：

```bash
# 本番環境依存関係
pip install -r requirements.txt --prefer-binary

# 開発環境依存関係（テストツールとコード品質ツールを含む）
pip install -r requirements-dev.txt --prefer-binary
```

> **注意**: `--prefer-binary`オプションを使用すると、Rustコンパイルの問題を回避するためにプリコンパイルされたバイナリパッケージが優先されます。Rust関連のエラーが発生する場合は、[Rustツールチェーン](https://www.rust-lang.org/tools/install)がインストールされていることを確認してください。

4. 環境変数の設定（または.envファイルの作成）：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=yoyaku
SECRET_KEY=your_secret_key
```

5. データベースの初期化：

```bash
python app/db/init_db.py
```

6. アプリケーションの起動：

#### 起動スクリプトの使用（推奨）

Windowsシステムでは、以下のバッチファイルをダブルクリックしてサービスを起動できます：

- `start-app.bat` - バックエンドAPIサービスの起動

起動スクリプトは、環境のチェック、仮想環境の作成、依存関係のインストール、およびサービスの起動を自動的に行います。

#### 手動起動

```bash
uvicorn main:app --reload --port 8000
```

サービスは http://localhost:8000 で起動し、APIドキュメントは http://localhost:8000/docs でアクセスできます。

## プロジェクト構造

```
yoyaku/
├── app/                      # コアアプリケーションコード
│   ├── api/                  # APIレイヤー
│   │   ├── dependencies/     # 共有依存関係（認証、権限など）
│   │   └── v1/               # APIバージョン1
│   │       ├── endpoints/    # リソースエンドポイント
│   │       └── router.py     # メインルーター設定
│   │
│   ├── core/                 # コア設定
│   │   ├── config.py         # 設定ファイル
│   │   ├── security.py       # セキュリティ関連
│   │   └── environment.py    # 環境設定
│   │
│   ├── db/                   # データベース関連
│   │   ├── base.py           # ベースモデルクラス
│   │   ├── session.py        # データベースセッション
│   │   └── init_db.py        # データベース初期化
│   │
│   ├── models/               # データベースモデル（ORM）
│   │
│   ├── schemas/              # Pydanticモデル（リクエスト/レスポンス）
│   │
│   ├── services/             # ビジネスロジックレイヤー
│   │
│   └── utils/                # 共通ユーティリティ関数
│
├── alembic/                  # データベースマイグレーション
│   └── versions/             # マイグレーションバージョン
│
├── sql/                      # SQLスクリプト
│   └── ddl.sql               # データベース定義
│
├── tests/                    # テストコード
│   ├── unit_test.py          # ユニットテスト
│   ├── integration_test.py   # 統合テスト
│   ├── test_setup.py         # テストデータセットアップ
│   └── testing_guide.md      # テストガイド
│
├── docs/                     # ドキュメント
│   ├── README_zh.md          # 中国語README
│   └── README_ja.md          # 日本語README（現在）
│
├── .env                      # 環境変数
│
├── .env.example              # 環境変数の例
│
├── .gitignore                # Gitの無視ファイル
│
├── .dockerignore             # Dockerの無視ファイル
│
├── alembic.ini               # Alembic設定
│
├── main.py                   # アプリケーションエントリーポイント
│
├── requirements.txt          # 本番環境依存関係
│
├── requirements-dev.txt      # 開発環境依存関係
│
└── start-app.bat             # バックエンドサービス起動スクリプト
```

## フロントエンドプロジェクト

このプロジェクトには、Vue 3とViteで構築された個別のフロントエンドリポジトリ `fitscheduler-frontend` があります。フロントエンドプロジェクトはAPIを通じてこのバックエンドプロジェクトと通信します。

フロントエンドプロジェクトリポジトリ: [FitScheduler Frontend](../../fitscheduler-frontend)

### フロントエンドプロジェクトの起動

フロントエンドプロジェクトは以下の方法で起動できます：

1. 起動スクリプトの使用（フロントエンドプロジェクトディレクトリ内）：
   - `start-frontend.bat` - フロントエンド開発サーバーの起動

2. 手動起動：
```bash
cd ../fitscheduler-frontend
npm install
npm run dev
```

フロントエンドサービスは http://localhost:5173 で起動します。

## API使用ガイド

### 認証

APIはJWTトークンを使用して認証を行います。トークンを取得する手順：

1. 新規ユーザーの登録：

```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "example_user",
  "password": "secure_password",
  "phone": "12345678901"
}
```

2. ログインしてトークンを取得：

```
POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

3. 後続のリクエストにトークンを使用：

```
Authorization: Bearer <your_token>
```

### 主要APIエンドポイント

- `/api/v1/auth/*` - 認証関連
- `/api/v1/users/*` - ユーザー管理
- `/api/v1/coaches/*` - コーチ管理
- `/api/v1/venues/*` - 施設管理
- `/api/v1/bookings/*` - 予約管理
- `/api/v1/reviews/*` - レビュー管理
- `/api/v1/lesson-types/*` - レッスンタイプ管理

完全なAPIドキュメントはアプリケーション実行後に `/docs` エンドポイントでアクセスできます。

## 開発ガイド

### コードスタイル

プロジェクトはPEP8コーディング規約に従い、FastAPI公式推奨のプロジェクト構造を使用しています。コード品質管理には以下のツールを推奨します：

- `black` - 自動コードフォーマット
- `flake8` - コードスタイルチェック

これらのツールは `requirements-dev.txt` に含まれています。

### 新機能の追加

1. **新しいデータベースモデルの作成**: `app/models/` ディレクトリで作成

2. **Pydanticスキーマの定義**: `app/schemas/` ディレクトリでリクエストとレスポンススキーマを作成

3. **サービスロジックの実装**: `app/services/` ディレクトリにビジネスロジックを追加

4. **APIエンドポイントの作成**: `app/api/v1/endpoints/` ディレクトリに新しいルートを追加

### テストの実行

まず、開発環境の依存関係がインストールされていることを確認します：

```bash
pip install -r requirements-dev.txt
```

次に、以下のコマンドを使用してテストを実行します：

```bash
python tests/test_setup.py  # テストデータを作成
pytest tests/unit_test.py   # ユニットテストを実行
pytest tests/integration_test.py  # 統合テストを実行
```

### データベースマイグレーション

Alembicを使用してデータベースマイグレーションを行います：

```bash
# マイグレーションスクリプトの作成
alembic revision --autogenerate -m "変更の説明"

# マイグレーションの適用
alembic upgrade head
```

## 貢献ガイドライン

プルリクエストとイシューの報告を歓迎します。コードがすべてのテストに合格し、プロジェクトのコーディング規約に従っていることを確認してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

## 言語

このドキュメントは複数の言語で利用可能です：
- [English](../README.md)
- [中文](README_zh.md)
- [日本語](README_ja.md)（現在） 