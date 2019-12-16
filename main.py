import speech_recognition as sr
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import threading
import win32com.client
import time

def direQuelqueChose(phraseDire):
    speaker.Speak(phraseDire)

def ecouteContinue() :
    r = sr.Recognizer()
    motCle = "Jarvis"
    entendu = -1
    print('le mot clé est : ', motCle)
    while entendu == -1 :
        with sr.Microphone() as source :
            try :
                print("En attente")
                audio = r.listen(source)
            except sr.UnknownValueError and sr.RequestError as e :
                print('')
        try:
            entendu = r.recognize_google(audio, language="fr-FR")
            entendu = entendu.find("Jarvis")
        except sr.UnknownValueError :
            print('')
    r = sr.Recognizer()
    global tache
    with sr.Microphone() as source :
        try :
            print("Je vous écoute")
            dire = threading.Thread(target=direQuelqueChose, args=("Je vous écoute",))  # crée un thread
            dire.start()
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            pass
    tache = r.recognize_google(audio, language="fr-FR")



def meteo():
    meteo = tache.find("météo")
    temps = tache.find("temps")
    if meteo != -1 or temps != -1 :
        meteoDuJour()

def meteoDuJour():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            dire = threading.Thread(target=direQuelqueChose, args=("De quel lieu voulez-vous connaitre la météo ?",))  # crée un thread
            dire.start()
            print('De quel lieu voulez-vous connaitre la météo ?')
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            pass
    lieu = r.recognize_google(audio, language="fr-FR")
    lieu = lieu.replace(' ', '-')
    ### On recupere les informations de meteo du jours
    url="http://api.openweathermap.org/data/2.5/weather?q=" + lieu + ",fr&appid=13e83287d3960d70d1a644490c1662c0&units=metric"
    content = requests.get(url)
    data=content.json()
    try :
        t = data["main"]['temp']
        d = data["weather"][0]['icon']

        ### On s'occupe de la temperature
        temps = "La température est de " + str(round(t)) + " degrés"

        ### On s'occupe de l'etat du ciel
        ciel = {'01': 'le ciel est degagé', '02': 'Il y a quelques nuages',  '03': 'Le ciel est nuageux', '04': 'Le ciel est très nuageux', '09': 'Il y a de fortes pluies', '10': 'Il pleut',  '11': "Il y a de l'orage", '13': 'Il neige', '50': 'Il y a du brouillard'}
        if d[2] == 'n':
            meteo = 'Il fait nuit, ' + ciel[d[0:2]]
        else :
            meteo = ciel[d[0:2]]

        ### On affiche la meteo
        print(temps)
        print(meteo)
        dire = threading.Thread(target=direQuelqueChose, args=(temps + meteo,))  # crée un thread
        dire.start()
    except KeyError:
        dire = threading.Thread(target=direQuelqueChose, args=('lieu introuvable',))  # crée un thread
        dire.start()
        print('lieu introuvable')
        meteoDuJour()



def video() :
    video = tache.find("vidéo")
    if video != -1 :
        lectureVideo()
        finVideo = threading.Thread(target=fermetureVideo)  # crée un thread
        finVideo.start()
        print('video lance')

def lectureVideo():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            dire = threading.Thread(target=direQuelqueChose, args=('Quelle video voulez vous regarder ?',))  # crée un thread
            dire.start()
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            pass
    sujet = r.recognize_google(audio, language="fr-FR")
    sujet = sujet.replace(' ', '+')
    ### On fait une recherche sur youtube
    url = 'https://www.youtube.com/results?search_query=' + sujet + '&sp=EgIQAQ%253D%253D'

    ### On recupere le fichier html de la page
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    ### On recupere le bloc html de la premiere video
    video = html.findAll('a')[50]

    ### On recupere le lien de la premiere video
    lien = video['href']

    ### On recupere la duree de la video au format H:MM:S
    global duree
    duree = html.findAll('span')[155].string

    ### On transfome la duree au format S
    if duree.count(':') == 1:
        duree = '00:' + duree
    dureeH, dureeM, dureeS = duree.split(':')

    duree = int(dureeH) * 3600 + int(dureeM) * 60 + int(dureeS)

    ### On lance la video dans le navigateur
    webbrowser.open('https://www.youtube.com' + lien + '#t=0h0m00s')

def fermetureVideo ():
    ### On attend la duree de la video
    time.sleep(duree)

    ### On ferme le navigateur
    os.system("taskkill /im chrome.exe /f")



def stop():
    stop = tache.find("stop")
    if stop != -1 :
        i=0
        return i

speaker = win32com.client.Dispatch("SAPI.SpVoice")

i=1
while i==1 :
    ecouteContinue()
    meteo()
    video()
    stop()
