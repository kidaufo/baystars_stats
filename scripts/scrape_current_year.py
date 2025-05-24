#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from baystars_scraper_base import BaystarsScraperBase

class BaystarsCurrentYearScraper(BaystarsScraperBase):
    """横浜DeNAベイスターズの今年の試合結果をスクレイピングするクラス"""
    
    def __init__(self):
        """初期化 - 今年のみを対象とする"""
        super().__init__()
        self.current_year = datetime.datetime.now().year
    
    def scrape_current_year(self):
        """今年のデータのみを取得して保存"""
        year = self.current_year
        html_content = self.fetch_year_data(year)
        
        if not html_content:
            print(f"{year}年のデータ取得に失敗しました")
            return None
            
        games = self.parse_game_data(html_content)
        print(f"{year}年: {len(games)}試合のデータを取得")
        
        # 今年のデータのみを含む辞書を作成
        current_year_data = {
            str(year): games
        }
        
        # 今年データ用のJSONファイルとして保存
        self.save_data(current_year_data, "current_year_data.json")
        return current_year_data

if __name__ == "__main__":
    scraper = BaystarsCurrentYearScraper()
    scraper.scrape_current_year()
