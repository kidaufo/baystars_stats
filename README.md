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
│   ├── baystars_net_wins.json  # 元データ
│   └── processed_data.json     # 処理済みデータ
├── scripts/                # Pythonスクリプト
│   ├── scraper.py          # データ収集スクリプト
│   └── data_processor.py   # データ処理スクリプト
├── web/                    # Webアプリケーション
│   ├── css/                # スタイルシート
│   │   └── style.css
│   ├── js/                 # JavaScriptファイル
│   │   ├── main.js         # メインスクリプト
│   │   └── plot_data.js    # 可視化データ
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
   python scraper.py
   python data_processor.py
   ```

4. ウェブサーバーを起動
   ```
   cd ../web
   python -m http.server
   ```

5. ブラウザで `http://localhost:8000` にアクセス

### GitHub Pagesでの公開

1. リポジトリの設定から GitHub Pages を有効化
2. Source を `main` ブランチの `/docs` フォルダに設定
3. `web` フォルダの内容を `docs` フォルダにコピー

## 自動更新

GitHub Actionsを使用して、毎日データを自動更新するように設定されています。
`.github/workflows/daily-update.yml` ファイルで設定を確認・変更できます。

## データソース

データは[プロ野球データFreak](https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php)から取得しています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 免責事項

このプロジェクトは非公式のファンサイトであり、横浜DeNAベイスターズおよび日本プロ野球機構とは関係ありません。