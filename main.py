import subprocess
import datetime
from mycalendar import process_glucose, create_calendar, add_event,write_calendar
import sys
import json
from utilities import createRestrictions, createGames, createDNF

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
        
    restrictions = createRestrictions(tournament_days,games_per_day,number_of_players)
    createDNF(restrictions,all_games)
    variables = process_glucose()
    calendar = create_calendar(tournament_name,start_date,end_date)

    players_map = {}
    days_map = {}
    hours_map = {}
    for i in range(number_of_players):
        players_map[i] = participants[i]
    for i in range(tournament_days):
        days_map[i] = start_date + datetime.timedelta(days=i)
    for i in range(games_per_day):
        begin = datetime.datetime.combine(start_date + datetime.timedelta(days=i), start_time)
        begin += datetime.timedelta(hours=i*2)
        hours_map[i] = begin.time()


    solution_file = open("salida_glucose.txt", "r")
    solution = solution_file.readline().strip()
    solution_file.close()
    for sol in solution.split():
        if int(sol) > 0:
            tuple = all_games[int(sol)]
            #print("---------")
            #print(tuple)
            #print(f"Local {players_map[tuple[0]]} vs visitante: {players_map[tuple[1]]}")
            #print(f"El día {days_map[tuple[2]]} a las {hours_map[tuple[3]]}")
            event = add_event(players_map[tuple[0]],players_map[tuple[1]],days_map[tuple[2]],hours_map[tuple[3]])
            calendar.add_component(event)

    write_calendar(calendar)
            



    #create_calendar(variables,tournament_name,start_date,end_date,participants,start_time)