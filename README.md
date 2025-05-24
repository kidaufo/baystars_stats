# 横浜DeNAベイスターズ 貯金数推移ビジュアライザー

このプロジェクトは横浜DeNAベイスターズの過去5年間（2020年〜現在）の貯金数（勝利数-敗戦数）の推移をインタラクティブに可視化するウェブアプリケーションです。

![サンプル画像](https://via.placeholder.com/800x400?text=横浜DeNAベイスターズ+貯金数推移ビジュアライザー)

## 機能

- 2020年から現在までの横浜DeNAベイスターズの貯金数推移を時系列グラフで表示
- 各年度のデータを異なる色の線で表示し、比較可能
- 各試合の詳細情報（日付、対戦相手、スコア）をホバーで確認可能
- 表示する年度の切り替え機能
- インタラクティブな操作（ホバーで詳細表示、ズーム、年度別表示切替など）
- レスポンシブデザイン（PC、タブレット、スマートフォン対応）
- GitHub Pagesでの公開に対応

## 技術スタック

- **バックエンド**: Python
  - BeautifulSoup4: Webスクレイピング
  - Plotly: データ可視化
- **フロントエンド**: HTML, CSS, JavaScript
  - Plotly.js: インタラクティブグラフ
- **自動化**: GitHub Actions

## プロジェクト構成

```
baseball_stats/
├── data/                   # データファイル
│   ├── historical_data.json    # 過去年度（2020-2024）のデータ
│   ├── current_year_data.json  # 今年（2025年）のデータ
│   └── processed_data.json     # 処理済みデータ
├── scripts/                # Pythonスクリプト
│   ├── baystars_scraper_base.py # スクレイピング基底クラス
│   ├── scrape_historical_data.py # 過去データ収集スクリプト
│   ├── scrape_current_year.py  # 今年のデータ収集スクリプト
│   ├── scraper.py          # 旧データ収集スクリプト（参考用）
│   └── data_processor.py   # データ処理スクリプト
├── docs/                   # GitHub Pages公開用ディレクトリ
│   ├── css/                # スタイルシート
│   │   └── style.css
│   ├── js/                 # JavaScriptファイル
│   │   ├── main.js         # メインスクリプト
│   │   └── plot_data.js    # 可視化データ（自動更新）
│   └── index.html          # メインHTML
├── .github/                # GitHub関連ファイル
│   └── workflows/          # GitHub Actions
│       └── daily-update.yml # 日次更新ワークフロー
├── requirements.txt        # Pythonパッケージ依存関係
└── README.md               # このファイル
```

## 使い方

### ローカルでの実行

1. リポジトリをクローン
   ```
   git clone https://github.com/yourusername/baseball_stats.git
   cd baseball_stats
   ```

2. 必要なPythonパッケージをインストール
   ```
   pip install -r requirements.txt
   ```

3. データを更新（オプション）
   ```
   cd scripts
   # 過去データ（2020-2024）を取得（初回のみ必要）
   python scrape_historical_data.py
   # 今年（2025年）のデータを取得
   python scrape_current_year.py
   # データを処理して可視化
   python data_processor.py
   ```

4. ウェブサーバーを起動
   ```
   cd ../docs
   python -m http.server
   ```

5. ブラウザで `http://localhost:8000` にアクセス

### GitHub Pagesでの公開

1. リポジトリの設定から GitHub Pages を有効化
2. Source を `main` ブランチの `/docs` フォルダに設定

## 自動更新

GitHub Actionsを使用して、毎日今年（2025年）のデータを自動更新するように設定されています。
過去のデータ（2020-2024年）は変更されないため、初回のみ手動で取得します。

自動更新の流れ：
1. 毎日UTC 20:00（日本時間翌日朝5:00）に実行
2. 今年のデータのみを取得（`scrape_current_year.py`）
3. データを処理して可視化（`data_processor.py`）
4. 変更があれば自動的にコミットしてプッシュ
5. GitHub Pagesに反映

設定は`.github/workflows/daily-update.yml`ファイルで確認・変更できます。

## データソース

データは[プロ野球データFreak](https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php)から取得しています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 免責事項

このプロジェクトは非公式のファンサイトであり、横浜DeNAベイスターズおよび日本プロ野球機構とは関係ありません。
