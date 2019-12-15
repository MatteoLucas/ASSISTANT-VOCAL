import random
import sys
from threading import Thread
import time

class Afficheur(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, lettre):
        Thread.__init__(self)
        self.lettre = lettre

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        sys.stdout.write(self.lettre)
        if self == 1 :
            sys.stdout.write('hello')
            sys.stdout.flush()
            time.sleep(5)
            sys.stdout.write('Bye')
            sys.stdout.flush()

        else :
            i = 0
            while i < 20:
                sys.stdout.write(str(i))
                sys.stdout.flush()
                time.sleep(1)
                i += 1

# Création des threads
thread_1 = Afficheur("1")
thread_2 = Afficheur("2")

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()