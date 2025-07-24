import json
import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import quote
from dataclasses import asdict

from basketball_reference.Configeration import PLAYER_BASE_URL, GameType, FIELD_MAPPING_HTML_TO_PlayerCareerPerGameStats
from basketball_reference.model.perGameData import PlayerCareerPerGameStats

def parse_player_url(name: str):
    words = name.lower().split()
    str = f"{words[1][0]}/{words[1][:5]}{words[0][:2]}01.html"
    print(str)
    return PLAYER_BASE_URL+str

def per_regular_game_data_career(name):
    return per_game_data_career(name,GameType.RS)

def per_playoffs_game_data_career(name):
    return per_game_data_career(name,GameType.PO)

def per_game_data_career(name: str,gameType:GameType):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = parse_player_url(name)
    print(url)

    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到常规赛数据表格
        if gameType == GameType.RS:
            tableID = 'per_game_stats'
        elif gameType == GameType.PO:
            tableID = 'per_game_stats_post'

        table = soup.find('table', {'id': tableID})

        if table:
            first_season_row = table.find("tbody").find("tr", id=True)
            row_id = first_season_row.get("id")
            career_per_game_raw = table.find("tfoot").find("tr", id=row_id)
            
            data = {
                class_field: career_per_game_raw.find(attrs={'data-stat': html_attr}).get_text(strip=True)
                for html_attr, class_field in FIELD_MAPPING_HTML_TO_PlayerCareerPerGameStats.items()
            }
            return PlayerCareerPerGameStats(**data)
        else:
            print(f"未找到常规赛数据表格: {url}")
            return None
        
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return None

if __name__ == "__main__":
    player_name = input().strip()
    data = per_playoffs_game_data_career(player_name)
    stats_dict = asdict(data)
    for key, value in stats_dict.items():
        print(f"{key}: {value}")

