import speech_recognition as sr


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
    with sr.Microphone() as source :
        print("Dites quelque chose")
        audio = r.listen(source)
    tache = r.recognize_google(audio, language="fr-FR")
    print("vous avez dit : ", tache)

tache = ''
ecouteContinue()