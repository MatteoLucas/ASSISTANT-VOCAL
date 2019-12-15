import speech_recognition as sr
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import threading
import subprocess
import win32com.client
import time
speaker = win32com.client.Dispatch("SAPI.SpVoice")


class video(threading.Thread) :

    def __init__(self):    # event = objet Event
        threading.Thread.__init__(self)  # = donnée supplémentaire
        self.videoLance = False

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                    speaker.Speak("Quelle video voulez vous regarder ?")
                    audio = r.listen(source)
            except sr.UnknownValueError and sr.RequestError as e:
                    print('')
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
        duree = html.findAll('span')[155].string

        ### On transfome la duree au format S
        if duree.count(':') == 1:
            duree = '00:' + duree
        dureeH, dureeM, dureeS = duree.split(':')

        duree = int(dureeH) * 3600 + int(dureeM) * 60 + int(dureeS)

        ### On lance la video dans le navigateur
        webbrowser.open('https://www.youtube.com' + lien + '#t=0h0m00s')

        ### On attend la duree de la video
        time.sleep(duree)

        ### On ferme le navigateur
        os.system("taskkill /im chrome.exe /f")

        subprocess.run(["python", "main.py"])


def ecouteContinue() :
    r = sr.Recognizer()
    motCle = "Jarvis"
    entendu =''
    print('le mot cle est : ', motCle)
    while entendu != motCle :
        with sr.Microphone() as source :
            try :
                print("En attente")
                audio = r.listen(source)
            except sr.UnknownValueError and sr.RequestError as e :
                print('')
        try:
            entendu = r.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError :
            print('')
    ecoutePrecise()

def ecoutePrecise() :
    r = sr.Recognizer()
    global tache
    with sr.Microphone() as source :
        try :
            print("Je vous écoute")
            speaker.Speak("Je vous écoute")
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            print('')
    tache = r.recognize_google(audio, language="fr-FR")

i=1
while i==1 :
    ecouteContinue()

    meteo = tache.find("météo")
    temps = tache.find("temps")
    if meteo != -1 or temps != -1 :
        os.system("Meteo.py")

    video = tache.find("vidéo")
    if video != -1 :
        videoLance = threading.Event()
        videoLance.clear()
        m = video(videoLance)  # crée un thread
        m.start()
        print("vous avez dit : ", tache)
        videoLance.wait()
        print('video lance')