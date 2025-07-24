import json
import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import quote

from ...Configeration import PLAYER_BASE_URL

def parse_player_url(name: str):
    words = name.lower().split()
    str = words[1][0]+"/"+words[1][:5]+words[0][:2]+"01.html"
    print(str)
    return PLAYER_BASE_URL+str

def per_game_data_career(name,seasonType):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = parse_player_url(name)

    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取球员姓名
        player_name = soup.find('h1', {'itemprop': 'name'}).get_text().strip()
        
        # 找到常规赛数据表格
        
        table = soup.find('table', {'id': 'per_game_stats'})
        
        if table:
            # 将HTML表格转换为DataFrame
            df = pd.read_html(str(table))[0]
            
            # 清理数据 - 移除多级表头和汇总行
            df.columns = df.columns.droplevel() if isinstance(df.columns, pd.MultiIndex) else df.columns
            df = df[df['Season'] != 'Career']
            df = df[df['Season'] != 'Season']
            
            # 添加球员姓名列
            df['Player'] = player_name
            
            return df
        else:
            print(f"未找到常规赛数据表格: {url}")
            return None
        
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return None


