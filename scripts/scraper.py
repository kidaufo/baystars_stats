#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
from pathlib import Path

class BaystarsScraper:
    """横浜DeNAベイスターズの試合結果をスクレイピングするクラス"""
    
    BASE_URL = "https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php"
    TEAM_CODE = "DB"  # 横浜DeNAベイスターズのチームコード
    
    def __init__(self, start_year=2020, end_year=None):
        """
        初期化
        
        Parameters:
        -----------
        start_year : int
            データ取得開始年
        end_year : int
            データ取得終了年（指定がない場合は現在の年）
            
        Notes:
        ------
        - 2025年のデータを取得する場合は、特別に y=0 パラメータを使用します
        - シーズン進行中の年は、当然ながら途中までの結果のみが取得されます
        """
        self.start_year = start_year
        self.end_year = end_year or datetime.datetime.now().year
        # 現在のスクリプトからの相対パスで data ディレクトリを指定
        script_dir = Path(__file__).parent.absolute()
        self.data_dir = script_dir.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def fetch_year_data(self, year):
        """指定した年のデータを取得"""
        print(f"{year}年のデータを取得中...")
        
        # 2025年の場合は特別に y=0 を使用する
        y_param = 0 if year == 2025 else year
        
        params = {
            "y": y_param,
            "leg": 0,  # 全試合
            "tm": self.TEAM_CODE,
            "mon": 0,  # 全月
            "vst": "all"  # 全対戦相手
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.encoding = 'utf-8'  # 日本語対応
        
        if response.status_code != 200:
            print(f"エラー: {response.status_code}")
            return None
        
        return response.text
    
    def parse_game_data(self, html_content):
        """HTMLから試合データを抽出"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # クラス 'Base' を持つテーブルを探す
        table = soup.find('table', class_='Base')
        if not table:
            print("テーブルが見つかりませんでした")
            return []
        
        games = []
        rows = table.find_all('tr')
        
        # ヘッダー行をスキップ (class='Index' または 'Index2' を持つ行)
        data_rows = [row for row in rows if not row.has_attr('class') or ('Index' not in row['class'] and 'Index2' not in row['class'])]
        
        for row in data_rows:
            cells = row.find_all('td')
            if len(cells) < 15:  # 必要なセル数が揃っているか確認
                continue
            
            try:
                # 中止された試合をスキップ
                if '中止' in row.text:
                    continue
                
                # 日付
                date_str = cells[0].text.strip()
                
                # 対戦相手 (3列目)
                opponent = cells[2].text.strip()
                
                # 球場 (4列目)
                location = cells[3].text.strip()
                
                # ホーム/ビジター (5列目)
                home_away = "H" if "Ｈ" in cells[4].text.strip() else "V"
                
                # 先発投手 (8列目)
                pitcher = cells[7].text.strip()
                
                # 勝敗 (17列目)
                result = cells[17].text.strip()
                
                # 未実施の試合（結果が空）はスキップ
                if not result:
                    continue
                
                # スコア (18列目)
                score = cells[18].text.strip()
                
                # 勝敗／貯 (21列目)
                record_text = cells[21].text.strip()
                
                # 勝敗／貯 から勝利数、敗戦数、引き分け数、貯金/借金を抽出
                import re
                
                # パターン1: 引き分けありの形式 例: "9(1)10 -1" (9勝10敗1分け、貯金-1)
                draws_pattern = re.search(r'(\d+)\((\d+)\)(\d+)\s*([+-]?\d+)', record_text)
                
                # パターン2: 標準形式 例: "1 - 0 +1" (1勝0敗、貯金+1)
                standard_pattern = re.search(r'(\d+)\s*-\s*(\d+)\s*([+-]?\d+)', record_text)
                
                if draws_pattern:
                    # 引き分けありの形式
                    wins = int(draws_pattern.group(1))
                    draws = int(draws_pattern.group(2))
                    losses = int(draws_pattern.group(3))
                    net_wins = int(draws_pattern.group(4))
                elif standard_pattern:
                    # 標準形式
                    wins = int(standard_pattern.group(1))
                    losses = int(standard_pattern.group(2))
                    net_wins = int(standard_pattern.group(3))
                    draws = 0
                else:
                    # どちらのパターンにも一致しない場合
                    print(f"勝敗記録のパースに失敗: {record_text}")
                    wins = 0
                    losses = 0
                    draws = 0
                    net_wins = 0
                
                # 日付をパース
                date_parts = date_str.split('/')
                if len(date_parts) >= 2:
                    month = int(date_parts[0])
                    day = int(date_parts[1])
                else:
                    continue
                
                game = {
                    "date": f"{month}/{day}",
                    "opponent": opponent,
                    "location": location,
                    "home_away": home_away,
                    "pitcher": pitcher,
                    "result": result,
                    "score": score,
                    "wins": wins,
                    "losses": losses,
                    "draws": draws,
                    "net_wins": net_wins
                }
                games.append(game)
            except Exception as e:
                print(f"データ解析エラー: {e}")
                continue
        
        return games
    
    
    def scrape_all_years(self):
        """全年度のデータを取得して保存"""
        all_data = {}
        
        for year in range(self.start_year, self.end_year + 1):
            html_content = self.fetch_year_data(year)
            if html_content:
                games = self.parse_game_data(html_content)
                all_data[str(year)] = games
                print(f"{year}年: {len(games)}試合のデータを取得")
            else:
                print(f"{year}年のデータ取得に失敗")
        
        # JSONとして保存
        output_path = self.data_dir / "baystars_net_wins.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"データを {output_path} に保存しました")
        return all_data

if __name__ == "__main__":
    scraper = BaystarsScraper()
    scraper.scrape_all_years()
