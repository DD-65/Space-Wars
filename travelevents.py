import random
from objects import benutzbareobjekte
from settings import treibstoff, geld
class Event:
    def __init__(self, name, desc, effects, chance=0):
        self.name = name
        self.desc = desc
        self.effects = effects
        self.chance = chance

## HIER EVENTS HINZUFÜGEN // CONTRIBUTE HERE
# MUSTER: eine konstante TEXT_*** mit kurzbeschreibung, eine funktion ***eff mit auswirkungen
# neues event dann in die liste schreiben
# vielen dank für die mitarbeit :D
# Variablen:
# (1) Name: name des events; (2) desc: kurzbeschreibung des events; (3) effects: funktion mit den auswirkungen des events, etwa ob der spieler geld verlieren soll
# (4) chance (standard 0): nur angeben, falls das event eine andere chance als 1/(anzahl events) haben soll, chance in %
# (4) die chance darf nicht > 100% sein
TEXT_PIRATEN = ("- A L A R M  -", "Du wirst von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
TEXT_ALIEN_1 = ("- A L A R M -", "Dir begegnet ein vollkommen unbekanntes Raumschiff!\n Wer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
TEXT_ALIEN_2 = ("- A L A R M -", "Deine Sensoren spüren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
TEXT_WURMLOCH = ("- A L A R M -","Es erscheint plötzlich ein Wurmloch auf den Sensoren!\n Du verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")

def pirateneff():
    global geld
    # zufällige entscheidung, ob von einem objekt geraubt wird
    for i in range(0, len(benutzbareobjekte)):
        materialchance = random.randint(1, 100)
        if materialchance > 50:
            # falls die wahl auf das objekt fällt, wird die hälfte der ladung des objekts geraubt
            benutzbareobjekte[i].geladen //= 2
    # auch wird in jedem fall die hälfte des geldes geraubt
    geld //= 2

def alien1eff():
    pass

def alien2eff():
    for i in range(0,len(benutzbareobjekte)):
        # gewisse chance für jedes objekt, dass etwas hinzugefügt wird
        alienchance = random.randint(1,100)
        if alienchance < 75:
            # "zufällige" menge, die hinzugefügt wird
            anzahl = random.randint(1,5)*(random.randint(1,2)+random.randint(0,4))
            benutzbareobjekte[i].geladen += anzahl

def wurmlocheff():
    # der treibstoff wird um die hälfte reduziert
    treibstoff // 2

# objektdefinitionen
piraten = Event("Piratenüberfall",TEXT_PIRATEN, pirateneff())
alien1 = Event("UFO", TEXT_ALIEN_1, alien1eff())
alien2 = Event("Asteroid", TEXT_ALIEN_2, alien2eff())
wurmloch = Event("Wurmloch", TEXT_WURMLOCH, wurmlocheff())

events = [piraten, alien1, alien2, wurmloch]

def chance_nicht_null():
    liste = []
    liste2 = events
    for i in events:
        if i.chance != 0:
            liste.append(i)
    for i in liste:
        liste2.remove(i)
    return liste, liste2

def reiseevent():
    # chance, dass überhaupt etwas passiert
    chance = random.randint(0,100)
    if chance >= 15:
        # falls es keine events mit besonderen wahrscheinlichkeiten gibt,
        if chance_nicht_null()[0] == []:
            # wird einfach zufällig eins ausgewählt
            auswahl = random.randint(0, len(events))
            return events[auswahl]
        else:
            # sonst werden von 100% nach und nach alle "sonderchancen" abgezogen
            restchance = 100
            for i in chance_nicht_null()[0]:
                restchance -= i.chance
            # ist der übrige rest kleiner null, ist die wahrscheinlichkeitszusammenstellung nicht möglich.
            # nichts passiert
            if restchance < 0:
                pass
            else:
                # sonst wird eine zufällige zahl ausgesucht und geschaut, 
                # ob sie in die wahrscheinlichkeit der objekte mit "sonderwahrscheinlichkeit" fällt
                auswahl = random.randint(1, 100)
                x = len(chance_nicht_null()[0])
                while x != 0:
                    if auswahl <= chance_nicht_null()[0][x]:
                        return chance_nicht_null()[0][x]
                    x -= 1
                # ist dies nicht der fall, wird wie oben ein zufälliges ereignis aus den verbleibenden ausgewählt
                auswahl = random.randint(0, len(events))
                return chance_nicht_null[1][auswahl]
    else:
        # falls die wahrscheinlichkeit nicht zutrifft, passiert nichts
        pass


