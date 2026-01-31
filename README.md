📝 Flask BBS System (掲示板システム)
FlaskとSQLiteを使用した、シンプルで拡張性の高い掲示板アプリケーションです。 大学・スクールの課題要件（16CFP）を満たし、データベースの階層構造（板 > スレッド > 投稿）とユーザー認証を実装しています。

🚀 主な機能
ユーザー管理: 新規登録、ログイン、パスワードのセキュアなハッシュ化

掲示板（板）機能: カテゴリ別の板分け、板間の移動

スレッド機能: 各板内での新規スレッド作成、スレッド一覧表示

投稿・返信機能: スレッド内への投稿、および特定の投稿への返信（アンカー機能）

タイムスタンプ: すべてのスレッドと投稿に作成日時を自動付与

永続化: SQLiteデータベースによるデータの永続化

🛠 技術スタック
Backend: Python 3.9+, Flask

Database: SQLite (SQLAlchemy ORM)

Frontend: HTML5 (Jinja2), Bootstrap 5 (CSS)

Authentication: Flask-Login

📂 ディレクトリ構造
Plaintext
.
├── app.py              # メインアプリケーション・DBモデル・ルート定義
├── requirements.txt    # 依存ライブラリ一覧
├── templates/          # HTMLテンプレート
│   ├── base.html       # 共通レイアウト
│   ├── index.html      # 板一覧
│   ├── board.html      # スレッド一覧・新規作成
│   ├── thread.html     # 投稿・返信表示
│   └── register.html   # ログイン・ユーザー登録
└── README.md
⚙️ セットアップと実行方法
1. リポジトリのクローン
Bash
git clone <あなたのリポジトリURL>
cd <リポジトリ名>
2. ライブラリのインストール
Bash
pip3 install -r requirements.txt
3. アプリケーションの起動
Bash
python3 app.py
起動後、ブラウザで http://127.0.0.1:5000 にアクセスしてください。初回起動時にデータベースファイル (bbs.db) が自動生成され、サンプルデータが投入されます。
