import requests
from googletrans import Translator

lieu = "Rennes"
### On recupere les informations de meteo du jours
url="http://api.openweathermap.org/data/2.5/weather?q=" + lieu + ",fr&appid=13e83287d3960d70d1a644490c1662c0&units=metric"
content = requests.get(url)
data=content.json()
t = data["main"]['temp']
d = data["weather"][0]['description']
meteo = "The temperature is " + str(round(t)) + " degree celsius and there is " + str(d)
print(meteo)
### on traduit les informations de meteo
translator = Translator()
traduced = (translator.translate(meteo, src='en', dest='fr')).text + ' '

### si 'épars' apparait dans la traduction on le supprime
if traduced[-6: -1] == 'épars' :
    traduced = traduced.replace(traduced[-20: -1], ' quelques nuages')

### On affiche la meteo
print(traduced)
