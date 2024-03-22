import json, sys

from math import floor
from itertools import combinations

games_mapping = {}
restrictions = []


def getIDDict(game):
    for key, value in games_mapping.items():
        if game == value:
            return key
 
    return "key doesn't exist"

def getGame(key):
    if key in games_mapping:
        return games_mapping[key]

    return "key doesn't exist"    
 
"""
This creates all possible games for the data provided
"""
def createGames(number_players,number_days,number_hours):
    games = []
    for i in range(0,number_players):
        for j in range(0,number_players):
            if i != j:
                for d in range(0,number_days):
                    for h in range(0,(number_hours)):
                        #print(f"{i} {j} {d} {h}")
                        games.append((i,j,d,h))
    for i in range(len(games)):
        games_mapping[i+1] = games[i]
    #print(games_mapping)
    return games

def createRestrictions(number_days,number_hours,number_players,games):
    restrictions = []
    # Two games cannot happen at the same time
    for d in range(0,number_days):
        for h in range(0,(number_hours//2)+1):
            for i in range(0,number_players):
                for j in range(0,number_players):
                    if i != j:
                        for k in range(0,number_players):
                            for l in range(0,number_players):
                                if (k != i or l != j) and k != l:
                                    restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((k,l,d,h))} 0")

    # All teams must play two times each and only two times
    for i in range(number_players):
        for j in range(number_players):
            if i != j:
                for d in range(number_days):
                    for h in range((number_hours//2)+1):
                        a = f"-{getIDDict((i,j,d,h))}"
                        for d2 in range(d+1,number_days):
                            for h2 in range(number_hours):
                                restrictions.append(f"{a} -{getIDDict((i,j,d2,h2))}")

    # A team can't play as visitor or local two times in a row
    for i in range(number_players):
        for j in range(number_players):
            if i != j:
                for d in range(number_days):
                    for h in range((number_hours)):
                        for j2 in range(number_players):
                            if i != j2 and j2 != j:
                                for h2 in range(number_hours):
                                    restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((i,j2,d,h2))} 0")
                                    restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((j2,j,d,h2))} 0")

    # A team can only play almost once per day
    for d in range(number_days):
        for i in range(number_players):
            for j in range(number_players):
                if i != j:
                    for h in range((number_hours // 2) + 1):
                        for k in range(number_players):
                            if k != i:
                                for l in range((number_hours // 2) + 1):
                                    if k != j:
                                        restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((i,k,d,l))}")
                                        restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((k,j,d,l))}")
                                    
                                    restrictions.append(f"-{getIDDict((i,j,d,h))} -{getIDDict((k,i,d,l))}")

    print(restrictions)