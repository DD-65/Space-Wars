from planets import sonnensystem
## WINDOW SETTINGS
# TODO: window settings (einstellbare fenstergröße, einstellungen-fenster?)

## GAME SETTINGS
tankmodifier = 0
STARTGELD = 10000
STARTLADERAUM = 100
MAX_TREIBSTOFF = (100 + tankmodifier)
STARTSTERNSYSTEM = sonnensystem
STARTPLANET = STARTSTERNSYSTEM.startplanet
laderaum = STARTLADERAUM
geld = STARTGELD
treibstoff = MAX_TREIBSTOFF
## TRAVEL SETTINGS
EVENT_CHANCE = 20 # chance in % auf ein reiseevent

## TEXTS
# FEHLERMELDUNGEN
TEXT_NOFUEL = ("- A L A R M -","Du kannst nicht weiterreisen.\nDu hast zu wenig Sprit im Tank oder einen zu kleinen Tank für den Flug.\nDu kehrst um.\n")
TEXT_SAME_PLANET_FLIGHT = ("- F E H L E R -","Du kannst nicht in das Sternsystem reisen, in dem du dich befindest.")
TEXT_BOTH_BUY_BUTTONS = ("- F E H L E R -","Du kannst nicht <alles> und <Die Hälfte> auswählen.")
TEXT_SELLING_WHAT_YOU_DONT_OWN = ("- F E H L E R -","Du kannst nicht verkaufen, was du nicht besitzt.\n")
TEXT_NO_MONEY_LOADING_SPACE = ("- F E H L E R -","Du hast zu wenig Geld/platz im Laderaum.\n")
TEXT_NO_MONEY = ("- F E H L E R -","Du hast zu wenig Geld.\n")
TEXT_TANK_FULL = ("- F E H L E R -","Dein Tank ist bereits voll.\n")
# WARPTOR-TEXTE
TEXT_WARPTOR_NO_MONEY = ("- F E H L E R -","Du hast zu wenig Geld für eine Reise mit dem Warptor.\nEine Reise kostet 150000$.")
TEXT_WARPTOR_SUCCESS = ("- R E I S E I N F O -","Vielen Dank für die Reise mit Warptor Systems™!\nIn diesem neuen Sternsystem müssen sie auf neue Gefahren achten, aber es gibt auch neue Profitmöglichkeiten...")
# HILFETEXT
TEXT_TUTORIAL ="""Willkommen zu Space Wars!
Space Wars ist ein interstellarer Handelssimulator. Dein Ziel ist es, durch geschicktes Kaufen und Verkaufen so viel Gewinn wie möglich zu machen!
\nHier ein kurzes Tutorial:\nIn der Liste oben links findest du die Materialien, die an deinem jetzigen Standort angeboten werden.
Du kannst sie durch Anklicken auswählen und durch Klicken auf den gleichnamigen Button kaufen.\n\nIn der Liste oben rechts findest du dein Inventar.
Du kannst auch hier durch Anklicken auswählen und mit dem Button 'Verkaufen' verkaufen.
\nUnten links findest du eine weitere Liste mit deinen Möglichkeiten zum weiterfliegen.
Du kannst durch Klicken auswählen und mit dem Button 'Weiterfliegen' genau dies tun.\nMit dem Button 'Neues Spiel' startest du neu,
und mit dem Button 'Score hochladen' kannst du deinen Score (dein gesammeltes Geld) mit den 10 besten Spielern vergleichen und hochladen.
\nDanke fürs Spielen und viel Spaß!" 
"""

# TUTORIAL
TEXT_TUTORIAL = """Du hast ein Warptor gefunden! Ein Netz von Warptoren durchsetzt den bewohnten Weltraum.
Mit ihnen kannst du schnell von Sternsystem zu Sternsystem reisen. Beachte allerdings, dass diese Reisen nicht billig sind!
Du kannst einfach zu einem anderen Planeten in deinem jetzigen Sternsystem reisen, falls du nicht mit dem Warptor reisen willst.
"""
# REISETEXTE


## Klasse, um eigene Fehler (in python) zu erzeugen
class Error(Exception):
    pass
# fehler, falls (z.B.) in travel.py ein planet nicht gefunden wird
class PlanetNotFoundError(Error):
    pass