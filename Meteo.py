import requests
import win32com.client
import os
import speech_recognition as sr
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def meteoDuJour(lieu):
    ### On recupere les informations de meteo du jours
    url="http://api.openweathermap.org/data/2.5/weather?q=" + lieu + ",fr&appid=13e83287d3960d70d1a644490c1662c0&units=metric"
    content = requests.get(url)
    data=content.json()
    try :
        t = data["main"]['temp']
        d = data["weather"][0]['icon']

        ### On s'occupe de la temperature
        temp = "La température est de " + str(round(t)) + " degrés"

        ### On s'occupe de l'etat du ciel
        ciel = {'01': 'le ciel est degagé', '02': 'Il y a quelques nuages',  '03': 'Le ciel est nuageux', '04': 'Le ciel est très nuageux', '09': 'Il y a de fortes pluies', '10': 'Il pleut',  '11': "Il y a de l'orage", '13': 'Il neige', '50': 'Il y a du brouillard'}
        if d[2] == 'n':
            meteo = 'Il fait nuit, ' + ciel[d[0:2]]
        else :
            meteo = ciel[d[0:2]]

        ### On affiche la meteo
        print(temp)
        print(meteo)
        speaker.Speak(temp)
        speaker.Speak(meteo)
    except KeyError:
        speaker.Speak('lieu introuvable')
        os.system('python Meteo.py')


def connaitreLieu() :
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speaker.Speak("De quel lieu voulez-vous connaitre la météo ?")
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            print('')
    ecoute = r.recognize_google(audio, language="fr-FR")
    longueur = len(ecoute)
    lieu = ''
    for caractere in range(0, longueur):
        lettre = ord(ecoute[caractere])
        if lettre == 32:
            nouvelleLettre = 45
        else:
            nouvelleLettre = lettre
        lieu += chr(nouvelleLettre)
    meteoDuJour(lieu)



connaitreLieu()

