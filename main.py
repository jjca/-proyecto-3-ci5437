""" print(tournament_hours)
    n_participants = len(participants)
"""
import datetime
import sys
import json
from utilities import createRestrictions, createGames

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing Argument")
        exit(1)

    # Reads JSON file to transform into dictionary
    with open(sys.argv[1], 'r') as json_file:
        content = json.load(json_file)

    json_file.close()

    tournament_name = content["tournament_name"]
    start_date = datetime.date.fromisoformat(content["start_date"])
    end_date = datetime.date.fromisoformat(content["end_date"])
    start_time = datetime.time.fromisoformat(content["start_time"])
    end_time = datetime.time.fromisoformat(content["end_time"])
    participants = content["participants"]

    tournament_days = (end_date - start_date).days + 1
    tournament_hours = (datetime.datetime.combine(datetime.date.today(),end_time) - datetime.datetime.combine(datetime.date.today(),start_time)).seconds//3600
    games_per_day = tournament_hours // 2 
    number_of_players = len(participants) 
    all_games = createGames(number_of_players,tournament_days,games_per_day)
    #print(all_games)
    restrictions = createRestrictions(tournament_days,games_per_day,number_of_players,all_games)
    