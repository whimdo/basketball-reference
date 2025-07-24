from basketball_reference.utils.player.perGameData import per_regular_game_data_career,per_playoffs_game_data_career
from dataclasses import asdict

if __name__ == "__main__":
    player_name = input().strip()
    data = per_playoffs_game_data_career(player_name)
    stats_dict = asdict(data)
    for key, value in stats_dict.items():
        print(f"{key}: {value}")