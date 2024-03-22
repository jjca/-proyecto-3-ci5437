import subprocess
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from utilities import getGame

def process_glucose():
    #Recolect variables from CNF file
    glucose_command = ["./bin/glucose","-model","-verb=0","output.cnf","salida_glucose.txt"]
    subprocess.call(glucose_command)

    #Send and recolect data to/for glucose
    solution_file = open("salida_glucose.txt", "r")
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
def add_event(local,guest,start_date,start_time):
    date = datetime.combine(start_date,start_time)
    date_plus_hour = date + timedelta(hours=2)
    #print(date_plus_hour)
    #print(date)
    event = Event()
    event.add('summary',"{}(Local) vs {}(Visitante)".format(local,guest))
    event.add('dtstart',date)
    event.add('dtend',date_plus_hour)
    #print(event)
    return event


def create_calendar(tournament_name,start_date,end_date):
    
    calendar = Calendar()
    calendar.add('summary', tournament_name)
    calendar.add('dtstart',start_date)
    calendar.add('dtend', end_date)

    return calendar

def write_calendar(calendar):
    calendar_file = open("calendario.ics", "wb")
    calendar_file.write(calendar.to_ical())
    calendar_file.close()