from basketball_reference.utils.player.perGameData import per_regular_game_data_career,per_playoffs_game_data_career,per_game_data_season
from basketball_reference.Configeration import GameType
from dataclasses import asdict

if __name__ == "__main__":
    player_name = input()
    data = per_game_data_season(player_name,GameType.RS, "2015", "2015")
    print(data)