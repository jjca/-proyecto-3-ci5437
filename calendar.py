import subprocess
import icalendar
from datetime import datetime

#Recolectar variables del archivo CNF
glucose_command = ["./bin/glucose","-model","-verb=0","prueba.cnf","salida_cnf.txt"]
subprocess.call(glucose_command)

#Pasar datos a glucose
    #Recolectar datos de glucose
solution_file = open("salida_cnf.txt", "r")
variables = []

for line in solution_file.readlines():
    if line[0] == 'c':
        continue
    if line[0] == 's' and line[1:] == 'UNSATISFIABLE':
        break

    variables.extend(line.split()[1:-1])
solution_file.close()

#Traducir datos a formato icalendar

def var_to_event(var):
    #Deducir a Jorge
    event = Event()
    event.add('summary',"{}(Local) vs {}(Visitante)".format(#las variables q reemplazan))
    event.add('dtstart',#aquivalafechadeinicio)
    event.add('dtend',#aquivalafechadeFIN)

    return event

calendar = Calendar()
calendar.add('summary', #nombre del evento)
calendar.add('dtstart',#aquivalafechadeinicio)
calendar.add('dtend',#aquivalafechadeFIN)

for var in variables:
    calendar.add_component(var_to_event(var))

calendar_file = open("calendario.ics", "w")
calendar_file.write(calendar.to_ical())
calendar_file.close()