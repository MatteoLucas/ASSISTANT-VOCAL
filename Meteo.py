import requests
from googletrans import Translator

lieu = "Rennes"
### On recupere les informations de meteo du jours
url="http://api.openweathermap.org/data/2.5/weather?q=" + lieu + ",fr&appid=13e83287d3960d70d1a644490c1662c0&units=metric&lang=fr"
content = requests.get(url)
data=content.json()
t = data["main"]['temp']
d = data["weather"][0]['icon']

### On s'occupe de la temperature
temp = "La temperature est de " + str(round(t)) + " degrés"

### On s'occupe de l'etat du ciel
ciel = {'01': 'le ciel est degagé', '02': 'Il y a quelques nuages',  '03': 'Le ciel est nuageux', '04': 'Le ciel est tres nuageux', '09': 'Il y a de fortes pluies', '10': 'Il pleut',  '11': "Il y a de l'orage", '13': 'Il neige', '50': 'Il y a du brouillard'}
if d[2] == 'n':
    meteo = 'Il fait nuit, ' + ciel[d[0:2]]
else :
    meteo = ciel[d[0:2]]

### On affiche la meteo
print(temp)
print(meteo)

