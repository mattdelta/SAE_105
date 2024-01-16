from icalendar import Calendar
import csv
import re
import shutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
try:
    import colorama
except:
    print('Veuillez installer le module colorama\npip install colorama')

def parse_ics_to_csv_v5(ics_file_path, csv_file_path):
    # Lire ficiher ics
    with open(ics_file_path, 'rb') as file:
        calendar = Calendar.from_ical(file.read())

    # Extraire tous les cours qui contiennent TP ou DS TP du fichier ics
    events = [event for event in calendar.walk() if event.name == "VEVENT" and ("DS" in event.get('summary') or "DS TP" in event.get('summary') or "DSTP" in event.get('summary'))]

    # Ouvrir le fichier csv
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Subject", "Start Date", "End Date", "Group"])

        # Ecrire les évènements + détails dans le fichier csv
        for event in events:
            start = event.get('dtstart').dt
            start = start.strftime('%Y-%m-%d %H:%M') # supprimer les :00+00:00
            end = event.get('dtend').dt
            end = end.strftime('%Y-%m-%d %H:%M') # supprimer les :00+00:00
            subject = event.get('summary')

            description = event.get('description')
            description = description.replace('\r', ' ').replace(' ','')  # supprimer les cassures et espaces
            
    # On récupère les groupes de classes dans la description
            # Méthode pour récupérer les classes avec regex mais innefficace car ne récupère qu'un groupe

            """ match = re.search(r'\b(RT\w+|TD\w+)\b', description)
            group = ''
            if match:
                result = match.group(1)
                group = result
                print(group)
                #print(subject, start, end, group) """

            # On récupère les groupes de classes efficacement car on récupère tous les groupes du cours
            # Si il y en a 3, on récupère les 3

            lines = description.split('\n')

            group = ''
            for line in lines:
                 words = line.split()# Chaque ligne mis en liste
                 for word in words: # pour chaque ligne
                      if word.startswith('RT') or word.startswith('TD'): #Si la ligne de la description commence par TD ou RT (pour récup les groupes)
                          group = group + word + ';' # Le ';' sert à séparer quand il ya plusieurs groupes
            
            #On écrit le contenu dans le fichier csv
            writer.writerow([subject, start, end, group[:-1]]) # [:-1] pour supprimer le dernier ';' de la ligne

ics_file_path = 'ADECal.ics' # Emplacement du fichier ics
csv_file_path = 'test.csv'  # Emplacement du fichier csv que le programme crée
parse_ics_to_csv_v5(ics_file_path, csv_file_path) # On éxécute la fonction principale

dates2 = []
events2 = []

#Entrée utilisateur
groupe_choisie = input(f'{colorama.Fore.LIGHTBLUE_EX}Choisissez votre goupe parmis :\n\n{colorama.Fore.WHITE}RT1App,RT1Shannon1,RT1Shannon2,RT2Hamming,RT2Dijkstra,RT2-S4,RT2App,\nRT1-S1,TDBell,RT2-S3,RT1Huffman,RT1Turing,TDFourier\n\n{colorama.Fore.LIGHTBLUE_EX}Choix du groupe > {colorama.Fore.LIGHTCYAN_EX}')

print(f'\n{colorama.Fore.LIGHTWHITE_EX}NOM DU DS OU DSTP, DATE DEBUT, DATE FIN, GROUPE(S)')

#On retourne les DS et/ou DS TP du groupe choisi
for cours in open(csv_file_path,'r',encoding='utf-8').read().split('\n'):
    if groupe_choisie in cours:
        print(f'{colorama.Fore.WHITE}\n'+cours.replace(',',' , ').replace(';',' & ')) #replace esthétique 
        dates2.append(cours.split(',')[1])
        events2.append(cours.split(',')[0])

#Les dates pour le graphique
dates = [datetime.strptime(date, "%Y-%m-%d %H:%M") for date in dates2]

plt.figure(figsize=(10, 5))
plt.plot(dates, events2,'bo')

print(dates)

#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().xaxis.set_major_locator(mdates.MonthLocator()) 

plt.gcf().autofmt_xdate()

plt.title("Frise chronologique des événements")
plt.tight_layout()
plt.show() 