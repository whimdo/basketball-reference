import json
import os
import sys
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import quote
from dataclasses import asdict

from basketball_reference.Configeration import (
    PLAYER_BASE_URL, GameType, FIELD_MAPPING_HTML_TO_PlayerCareerPerGameStats,
    FIELD_MAPPING_HTML_TO_PlayerSeasonPerGameStats,HEADERS
)
from basketball_reference.model.perGameData import PlayerCareerPerGameStats,PlayerSeasonPerGameStats

def row_to_data(table, field_mapping: Dict[str, str]) -> Dict[str, str]:
    """
    Convert a BeautifulSoup table to a dictionary using the provided field mapping.
    """
    data = {}
    for html_attr, class_field in field_mapping.items():
        cell = table.find(attrs={'data-stat': html_attr})
        if cell:
            anchor = cell.find("a")
            text = anchor.get_text(strip=True) if anchor else cell.get_text(strip=True)
            data[class_field] = text
    return data

def get_player_id(name: str):
    words = name.lower().split()
    player_id = f"{words[1][:5]}{words[0][:2]}01"
    return player_id

def parse_player_url(name: str):
    words = name.split()
    str = f"{words[1][0].lower()}/{get_player_id(name)}.html"
    print(str)
    return PLAYER_BASE_URL+str

def parse_player_season_summary_url(name: str, gameType: GameType,startSeason: str, endSeason: str):
        player_id = get_player_id(name)
        if gameType == GameType.RS:
            phase_type = "reg"
        elif gameType == GameType.PO:
            phase_type = "post"
        else:
            raise ValueError("Unsupported game type")
        return (
        f"https://www.basketball-reference.com/tools/soc_player_season_summing.cgi?"
        f"html=1&page_id={player_id}&table_id=per_game_stats&"
        f"range={startSeason}-{endSeason}&plink=1&phase_type={phase_type}&"
        f"table_type=PlayerPerGame&entity_id={player_id}"
    )

def fetch_player_season_summary_html(name: str, gameType: GameType, startSeason: str, endSeason: str):
    url = parse_player_season_summary_url(name, gameType, startSeason, endSeason)
    print(url)

    header = {
        **HEADERS,
        'Referer': parse_player_url(name)
    }

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return None

def per_regular_game_data_career(name: str):
    """ 
    Get the career per game data for a player in regular season.
    :param name: Player's
    """
    return per_game_data_career(name,GameType.RS)

def per_playoffs_game_data_career(name: str):
    """
    Get the career per game data for a player in playoffs.
    :param name: Player's name
    """
    return per_game_data_career(name,GameType.PO)

def pre_regular_game_data_certain_season(name:str,Season:str):
    """
    Get the per game data for a player in regular season for a certain season.
    :param name: Player's name
    :param Season: Season in format 'YYYY'
    """
    return per_game_data_season(name,GameType.RS,Season,Season)

def pre_playoffs_game_data_certain_season(name:str,Season:str):
    """
    Get the per game data for a player in playoffs for a certain season.
    :param name: Player's name
    :param Season: Season in format 'YYYY'
    """
    return per_game_data_season(name,GameType.PO,Season,Season)

def per_regular_game_data_season(name:str,startSeason:str,endSeason:str):
    return per_game_data_season(name,GameType.RS,startSeason,endSeason)

def per_playoffs_game_data_season(name:str,startSeason:str,endSeason:str):
    return per_game_data_season(name,GameType.PO,startSeason,endSeason)

def per_game_data_career(name: str,gameType:GameType):

    url = parse_player_url(name)
    print(url)

    try:
        # 发送HTTP请求
        response = requests.get(url, headers=HEADERS)
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

def get_per_game_data_multi_season(name: str, gameType: GameType, startSeason: str, endSeason: str):
    url = parse_player_url(name)

    try:
        # 发送HTTP请求
        html = fetch_player_season_summary_html(name, gameType, startSeason, endSeason)
        # 解析HTML内容
        soup = BeautifulSoup(html, 'html.parser')
        
        # 找到常规赛数据表格
        if gameType == GameType.RS:
            tableID = 'per_game_stats_sum'
        elif gameType == GameType.PO:
            tableID = 'per_game_stats_post_post_sum'

        table = soup.find('table', {'id': tableID})
        if table:
            target_row = table.find("tbody").find("tr")
            data = row_to_data(target_row, FIELD_MAPPING_HTML_TO_PlayerSeasonPerGameStats)
            return PlayerSeasonPerGameStats(**data)
        else:
            print(f"未找到常规赛数据表格: {url}")
            return []
        
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return []

def get_per_game_data_single_season(name: str, gameType: GameType, Season: str):
    url = parse_player_url(name)
    print(url)
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=HEADERS)
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
            id = f'per_game_stats.{Season}'#查找到特定赛季的行
            target_row = table.find("tbody").find("tr", id=id)
            data = {}
            if not target_row:
                print(f"未找到赛季 {Season} 的数据行: {url}")
                return None
            else:
                data = row_to_data(target_row, FIELD_MAPPING_HTML_TO_PlayerSeasonPerGameStats)
            return PlayerSeasonPerGameStats(**data)
        else:
            print(f"未找到常规赛数据表格: {url}")
            return None
        
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return None

def per_game_data_season(name: str, gameType: GameType, startSeason: str, endSeason: str):
    """
    Get the per game data for a player in regular season or playoffs.
    :param name: Player's name
    :param gameType: GameType (Regular Season or Playoffs)
    :param startSeason: Start season in format 'YYYY'
    :param endSeason: End season in format 'YYYY'
    """
    if( startSeason == endSeason):
        return get_per_game_data_single_season(name, gameType, startSeason)
    return get_per_game_data_multi_season(name, gameType, startSeason, endSeason)

def per_game_detail_data_consecutive_seasons(name: str, gameType: GameType, startSeason: str, endSeason: str)-> List[PlayerSeasonPerGameStats]:
    """
    Get the detail per game data list for a player in regular season or playoffs for consecutive seasons.
    :param name: Player's name
    :param gameType: GameType (Regular Season or Playoffs)
    :param startSeason: Start season in format 'YYYY'
    :param endSeason: End season in format 'YYYY'
    """
    url = parse_player_url(name)
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=HEADERS)
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
            start_id = f'per_game_stats.{startSeason}'#查找到特定赛季的行
            end_id = f'per_game_stats.{endSeason}'
            
            tbody = table.find("tbody")
            row = tbody.find("tr", id=start_id)
            data_list: list[PlayerSeasonPerGameStats] = []

            while row:
                row_id = row.get("id", "")
                if row_id and row_id.startswith("per_game_stats."):
                    data = row_to_data(row, FIELD_MAPPING_HTML_TO_PlayerSeasonPerGameStats)
                    data_list.append(PlayerSeasonPerGameStats(**data))
                if row_id == end_id:
                    break
                row = row.find_next_sibling("tr")

            return data_list
        else:
            print(f"未找到常规赛数据表格: {url}")
            return None
        
    except Exception as e:
        print(f"获取数据时出错: {url} - {str(e)}")
        return None

