from enum import Enum


BASE_URL = "https://www.basketball-reference.com/"
PLAYER_BASE_URL = "https://www.basketball-reference.com/players/"
HEADERS= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


class GameType(Enum):
    RS = "Regular Season"
    PO = "Playoffs"
    PS = "Pre Season"


FIELD_MAPPING_HTML_TO_PlayerCareerPerGameStats = {
    'year_id': 'Years',          # HTML: data-stat="year_id" → 类字段: Years
    'games': 'G',                # HTML: data-stat="games" → 类字段: G
    'games_started': 'GS',       
    'mp_per_g': 'MP',
    'fg_per_g': 'FG',
    'fga_per_g': 'FGA',
    'fg_pct': 'FG_percent',
    'fg3_per_g': '_3P',
    'fg3a_per_g': '_3PA',
    'fg3_pct': '_3P_percent',
    'fg2_per_g': '_2P',
    'fg2a_per_g': '_2PA',
    'fg2_pct': '_2P_percent',
    'efg_pct': 'eFG_percent',
    'ft_per_g': 'FT',
    'fta_per_g': 'FTA',
    'ft_pct': 'FT_percent',
    'orb_per_g': 'ORB',
    'drb_per_g': 'DRB',
    'trb_per_g': 'TRB',
    'ast_per_g': 'AST',
    'stl_per_g': 'STL',
    'blk_per_g': 'BLK',
    'tov_per_g': 'TOV',
    'pf_per_g': 'PF',
    'pts_per_g': 'PTS'
}

FIELD_MAPPING_HTML_TO_PlayerSeasonPerGameStats = {
    'year_id': 'Season',          
    'age_range': 'Age',
    'age': 'Age',       
    'teams_played_for_career':'Team',
    'team_name_abbr': 'Team',  # HTML: data-stat="team_name_abbr" → 类字段: Team
    'comp_name_abbr': 'Lg',             
    'pos': 'Pos',                
    'games': 'G',                
    'games_started': 'GS',       
    'mp_per_g': 'MP',
    'fg_per_g': 'FG',
    'fga_per_g': 'FGA',
    'fg_pct': 'FG_percent',
    'fg3_per_g': '_3P',
    'fg3a_per_g': '_3PA',
    'fg3_pct': '_3P_percent',
    'fg2_per_g': '_2P',
    'fg2a_per_g': '_2PA',
    'fg2_pct': '_2P_percent',
    'efg_pct': 'eFG_percent',
    'ft_per_g': 'FT',
    'fta_per_g': 'FTA',
    'ft_pct': 'FT_percent',
    'orb_per_g': 'ORB',
    'drb_per_g': 'DRB',
    'trb_per_g': 'TRB',
    'ast_per_g': 'AST',
    'stl_per_g': 'STL',
    'blk_per_g': 'BLK',
    'tov_per_g': 'TOV',
    'pf_per_g': 'PF',
    'pts_per_g': 'PTS'
}
