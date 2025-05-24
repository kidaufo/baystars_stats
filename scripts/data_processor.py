#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

class BaystarsDataProcessor:
    """横浜DeNAベイスターズの貯金数データを処理するクラス"""
    
    def __init__(self):
        """初期化"""
        # 現在のスクリプトからの相対パスでディレクトリを指定
        script_dir = Path(__file__).parent.absolute()
        self.data_dir = script_dir.parent / "data"
        self.web_dir = script_dir.parent / "web"
        self.historical_file = self.data_dir / "historical_data.json"
        self.current_year_file = self.data_dir / "current_year_data.json"
        self.output_file = self.data_dir / "processed_data.json"
        
    def load_data(self):
        """過去データと今年のデータを読み込み、統合する"""
        all_data = {}
        
        # 過去データの読み込み
        if self.historical_file.exists():
            with open(self.historical_file, 'r', encoding='utf-8') as f:
                historical_data = json.load(f)
                all_data.update(historical_data)
            print(f"過去データを {self.historical_file} から読み込みました")
        else:
            print(f"警告: 過去データファイル {self.historical_file} が見つかりません")
        
        # 今年のデータの読み込み
        if self.current_year_file.exists():
            with open(self.current_year_file, 'r', encoding='utf-8') as f:
                current_year_data = json.load(f)
                all_data.update(current_year_data)
            print(f"今年のデータを {self.current_year_file} から読み込みました")
        else:
            print(f"警告: 今年のデータファイル {self.current_year_file} が見つかりません")
            
        if not all_data:
            print("エラー: データが読み込めませんでした")
            return None
            
        return all_data
    
    def process_data(self, data):
        """データを処理して可視化用に整形"""
        if not data:
            return None
        
        processed_data = {}
        current_year = datetime.datetime.now().year
        
        for year, games in data.items():
            # 各ゲームに通し番号を追加
            game_numbers = list(range(1, len(games) + 1))
            
            # 貯金数の配列を作成
            net_wins = [game["net_wins"] for game in games]
            
            # 日付の配列を作成
            dates = [game["date"] for game in games]
            
            # 対戦相手と結果の配列を作成
            opponents = [game["opponent"] for game in games]
            results = [game["result"] for game in games]
            scores = [game["score"] for game in games]
            
            # 年ごとのデータを格納
            processed_data[year] = {
                "game_numbers": game_numbers,
                "net_wins": net_wins,
                "dates": dates,
                "opponents": opponents,
                "results": results,
                "scores": scores,
                "is_current_year": year == str(current_year)
            }
        
        return processed_data
    
    def save_processed_data(self, processed_data):
        """処理したデータをJSONとして保存"""
        if not processed_data:
            return
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
        
        print(f"処理済みデータを {self.output_file} に保存しました")
    
    def create_plotly_visualization(self, processed_data):
        """Plotlyを使用して可視化を作成"""
        if not processed_data:
            return
        
        # プロットの作成
        fig = go.Figure()
        
        # 色の設定
        colors = {
            "2020": "#1f77b4",  # 青
            "2021": "#ff7f0e",  # オレンジ
            "2022": "#2ca02c",  # 緑
            "2023": "#d62728",  # 赤
            "2024": "#9467bd",  # 紫
            "2025": "#8c564b",  # 茶色
        }
        
        # 各年のデータをプロット
        for year, year_data in processed_data.items():
            game_numbers = year_data["game_numbers"]
            net_wins = year_data["net_wins"]
            dates = year_data["dates"]
            opponents = year_data["opponents"]
            results = year_data["results"]
            scores = year_data["scores"]
            is_current_year = year_data["is_current_year"]
            
            # ホバーテキストの作成
            hover_texts = []
            for i in range(len(game_numbers)):
                hover_text = f"{year}年 {dates[i]}<br>" + \
                             f"対戦: {opponents[i]}<br>" + \
                             f"結果: {results[i]} {scores[i]}<br>" + \
                             f"貯金: {net_wins[i]}"
                hover_texts.append(hover_text)
            
            # 線の太さと種類を設定
            line_width = 3 if is_current_year else 2
            line_dash = "solid"
            
            # マーカーサイズを設定
            marker_size = 10 if is_current_year else 6
            
            # 線のプロット
            fig.add_trace(go.Scatter(
                x=game_numbers,
                y=net_wins,
                mode='lines+markers',
                name=f'{year}年',
                line=dict(color=colors.get(year, "#000000"), width=line_width, dash=line_dash),
                marker=dict(size=marker_size),
                hovertext=hover_texts,
                hoverinfo="text"
            ))
        
        # レイアウトの設定
        fig.update_layout(
            title="横浜DeNAベイスターズ 貯金数推移 (2020-現在)",
            xaxis_title="試合数",
            yaxis_title="貯金数",
            hovermode="closest",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            template="plotly_white",
            font=dict(
                family="Meiryo, sans-serif",
                size=14
            )
        )
        
        # グリッド線の設定
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', zeroline=True, zerolinewidth=2, zerolinecolor='Gray')
        
        # HTMLとして保存
        html_path = self.web_dir / "js" / "plot_data.js"
        
        # Plotlyのグラフをオブジェクトとして保存
        plot_json = pio.to_json(fig)
        
        # JavaScriptファイルとして保存
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(f"const plotData = {plot_json};\n")
        
        print(f"可視化データを {html_path} に保存しました")
    
    def run(self):
        """データ処理の実行"""
        data = self.load_data()
        if data:
            processed_data = self.process_data(data)
            self.save_processed_data(processed_data)
            self.create_plotly_visualization(processed_data)
            return True
        return False

if __name__ == "__main__":
    processor = BaystarsDataProcessor()
    processor.run()
