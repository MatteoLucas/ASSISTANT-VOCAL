import speech_recognition as sr
import os
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")

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
        entendu = r.recognize_google(audio, language="fr-FR")
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
    print("vous avez dit : ", tache)


ecouteContinue()
meteo = tache.find("météo")
if meteo != -1 :
    os.system('python Meteo.py')