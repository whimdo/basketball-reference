from basketball_reference.utils.player.perGameData import per_regular_game_data_career,per_playoffs_game_data_career,per_game_data_season,per_game_detail_data_consecutive_seasons
from basketball_reference.Configeration import GameType
from dataclasses import asdict

if __name__ == "__main__":
    player_name = input()
    data = per_game_detail_data_consecutive_seasons(player_name,GameType.RS, "2015", "2019")
    for item in data:
        print(item)