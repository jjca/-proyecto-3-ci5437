import subprocess
from icalendar import Calendar, Event
from datetime import datetime
from utilities import getGame

def process_glucose():
    #Recolect variables from CNF file
    glucose_command = ["./bin/glucose","-model","-verb=0","prueba.cnf","salida_cnf.txt"]
    subprocess.call(glucose_command)

    #Send and recolect data to/for glucose
    solution_file = open("salida_cnf.txt", "r")
    variables = []

    for line in solution_file.readlines():
        if line[0] == 'c':
            continue
        if line[0] == 's' and line[1:] == 'UNSATISFIABLE':
            break

        variables.extend(line.split()[1:-1])
    solution_file.close()
    return variables

#Translate data to icalendar format
def var_to_event(var,participants,start_date,start_time):
    game = getGame(var)
    local = participants[game[0]]
    guest = participants[game[1]]
    day = start_date + datetime.timedelta(days= game[2])
    hour = start_time + datetime.timedelta(hours= game[3])

    event = Event()
    event.add('summary',"{}(Local) vs {}(Visitante)".format(local,guest))
    event.add('dtstart',day)
    event.add('dtend',hour)

    return event

def create_calendar(variables,tournament_name, start_time,end_time):
    
    calendar = Calendar()
    calendar.add('summary', tournament_name)
    calendar.add('dtstart',start_time)
    calendar.add('dtend', end_time)

    for var in variables:
        calendar.add_component(var_to_event(var))

    calendar_file = open("calendario.ics", "w")
    calendar_file.write(calendar.to_ical())
    calendar_file.close()