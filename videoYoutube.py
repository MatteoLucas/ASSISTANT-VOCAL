import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import subprocess
import time
import speech_recognition as sr
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def lancementVideo(sujet) :
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
    duree = video.span()[1].string

    ### On transfome la duree au format S

    if duree.count(':') == 1 :
        duree = '00:' + duree
    dureeH, dureeM, dureeS = duree.split(':')


    duree = int(dureeH) * 3600 + int(dureeM) * 60 + int(dureeS)

    ### On lance la video dans le navigateur
    webbrowser.open('https://www.youtube.com' + lien + '#t=0h0m00s')

    os.system("main.py")

    ### On attend la duree de la video
    time.sleep(duree)

    ### On ferme le navigateur
    os.system("taskkill /im chrome.exe /f")


def connaitreRecherche() :
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speaker.Speak("Quelle video voulez vous regarder ?")
            audio = r.listen(source)
        except sr.UnknownValueError and sr.RequestError as e:
            print('')
    sujet = r.recognize_google(audio, language="fr-FR")
    sujet = sujet.replace(' ','+')
    lancementVideo(sujet)

print('lol')
connaitreRecherche()