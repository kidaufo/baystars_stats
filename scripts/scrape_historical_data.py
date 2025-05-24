#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from baystars_scraper_base import BaystarsScraperBase

class BaystarsHistoricalScraper(BaystarsScraperBase):
    """横浜DeNAベイスターズの過去の試合結果をスクレイピングするクラス"""
    
    def __init__(self, start_year=2020, end_year=2024):
        """初期化 - 過去年度のみを対象とする (2020-2024)"""
        super().__init__()
        self.start_year = start_year
        self.end_year = end_year
    
    def scrape_historical_years(self):
        """過去年度のデータをまとめて取得して保存"""
        all_data = {}
        
        for year in range(self.start_year, self.end_year + 1):
            html_content = self.fetch_year_data(year)
            if html_content:
                games = self.parse_game_data(html_content)
                all_data[str(year)] = games
                print(f"{year}年: {len(games)}試合のデータを取得")
            else:
                print(f"{year}年のデータ取得に失敗")
        
        # 過去データ用のJSONファイルとして保存
        self.save_data(all_data, "historical_data.json")
        return all_data

if __name__ == "__main__":
    scraper = BaystarsHistoricalScraper()
    scraper.scrape_historical_years()
