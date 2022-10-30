# Imports
import imp
from planets import sternsysteme
from treibstoff import treibstoffverbrauch
from settings import PlanetNotFoundError, TEXT_NOFUEL, STARTPLANET, treibstoff
from travelevents import reiseevent
import tkinter

# anzahl der reisen
reiseanzahl = 0
# jetziger planet
standortplanet = STARTPLANET
# variable, um die infos nach einer reise nicht anzuzeigen
nichtanzeigen = False
# verknüpfen des importierten treibstoff mit variable
treibstofflocal = treibstoff

def system_des_planeten(testplanet) -> object:
    # gibt das sternsystem des planeten aus
    for system in sternsysteme:
        if testplanet in system.planeten:
            return system
    if True:
        raise PlanetNotFoundError("Dieser Planet befindet sich in keinem den Archiven bekannten Sternsystem.")

standortsystem = system_des_planeten(standortplanet)

def weiterfliegen(planetneu, planetalt):
    from game import warptorhide, treibstoffzustand
    global standortplanet, reiseanzahl, nichtanzeigen, treibstofflocal
    # falls man vom warptor wegfliegt, werden die GUI-Elemente wieder eingeblendet
    if planetalt.name == "Warptor":
        for point in warptorhide:
            point.grid()
    # zum gewünschten planeten reisen
    # überprüfen ob der planet existiert
    # (im moment unnötig, später bei manueller eingabe wichtig)
    try:
        planetneusystem = system_des_planeten(planetneu)
    except PlanetNotFoundError:
        # TODO: ädaquate reaktion auf dieses event
        pass
    # mit einer gewissen chance eine reiseaktion (z.B. piratenüberfall) auslösen 
    reiseevent()
    # eigentliche reise durchführen
    standortplanet = planetneu
    reiseanzahl += 1
    nichtanzeigen = False
    if standortplanet.warptor:
        # TODO: überleitung zu warptor.py bei ankunft an einem solchen
        pass
    # verbrauchten treibstoff abziehen
    abzug = treibstoffverbrauch(treibstoffzustand, planetalt, planetneu)
    # falls reise nicht möglich ist (=man hat danach keinen treibstoff mehr):
    # darauf hinweisen, ort ändern, treibstoff zurückerstatten & reiseinfos nicht anzeigen
    if treibstofflocal < 0:
        tkinter.messagebox.show(TEXT_NOFUEL)
        treibstofflocal += abzug
        nichtanzeigen = True
        standortplanet = planetalt
    # TODO: warptorcheck & warptor etc.
    # TODO: logs
