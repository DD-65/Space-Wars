import tkinter
import tkinter.messagebox as messagebox
from random import randint
from datetime import datetime
from time import sleep
from models import Planet, Planetensystem, Objekt

# ----------------------------
# Global game state variables
Geld = 10000         # STARTGELD DES SPIELERS
Laderaum = 100       # FREIER LADERAUM IM SCHIFF DES SPIELERS (AM ANFANG)
reisen = 0           # ANZAHL DER REISEN VON PLANET ZU PLANET
galaxienreisen = 0   # ANZAHL DER REISEN ZWISCHEN GALAXIEN (WARPTOR)
treibstoff = 100     # TREIBSTOFFFÜLLUNG
treibstoffmax = 100
erstereise = True

# ----------------------------
# Globals that will be set from gui.py
game = None
ListeObjekte = None
ListeLaderaum = None
ListeOrte = None
TreibstoffZustand = None
fotolabel = None
EingabeMenge = None
cb = None
halb = None
warptorhide = []  # List of widgets to hide when at a warp gate
locationImg = None

# ----------------------------
# Initialize planets and systems using models

# Sonnensystem planets (images are not loaded yet)
sonne = Planet("Sonne", "Milchstraße", 0, False, False, "./assets/fotos/ship.gif")
erde = Planet("Erde", "Milchstraße", 250, False, True, "./assets/fotos/erde.gif")
mars = Planet("Mars", "Milchstraße", 370, False, True, "./assets/fotos/mars.gif")
venus = Planet("Venus-Raumstation", "Milchstraße", 100, False, True, "./assets/fotos/venus.gif")
uranus = Planet("Uranus-Raumstation", "Milchstraße", 600, False, True, "./assets/fotos/uranus.gif")
pluto = Planet("Pluto", "Milchstraße", 1100, False, True, "./assets/fotos/pluto.gif")
warptorS = Planet("Warptor", "Milchstraße", 1000, True, True, "./assets/fotos/warp.gif")
sPlaneten = [sonne, erde, mars, venus, uranus, pluto, warptorS]

# Alpha Centauri planets
alphacentauria = Planet("Alpha Centauri A (Stern)", "Alpha Centauri", 0, False, False, "./assets/fotos/ship.gif")
alphacentauriab = Planet("Alpha Centauri Ab", "Alpha Centauri", 150, False, True, "./assets/fotos/ship.gif")
alphacentauribb = Planet("Alpha Centauri Bb", "Alpha Centauri", 2580, False, True, "./assets/fotos/ship.gif")
warptorA = Planet("Warptor", "Alpha Centauri", 1000, True, True, "./assets/fotos/warp.gif")
aPlaneten = [alphacentauria, alphacentauriab, alphacentauribb, warptorA]

# Define Planetensysteme
sonnensystem = Planetensystem("Sonnensystem", sPlaneten, erde)
alphacentauri = Planetensystem("Alpha Centauri", aPlaneten, alphacentauria)
sternsysteme = [sonnensystem, alphacentauri]

# Current state in the game
sternsystem = sonnensystem  # Aktuelles Sternsystem
Ort = sternsystem.startplanet  # Aktueller Planet

# ----------------------------
# Define objects (tradable items)
objekte = []
eisen = Objekt("Eisen", 250, 1350, 100, 0, sonnensystem, True, True)
h2o = Objekt("H2O", 750, 1700, 200, 0, sonnensystem, True, True)
co2 = Objekt("CO2", 600, 2000, 200, 0, sonnensystem, True, True)
titan = Objekt("Titan", 380, 1800, 150, 0, sonnensystem, True, True)
lithium = Objekt("Lithium", 1000, 7500, 400, 0, sonnensystem, True, True)
treibstoffobj = Objekt("Treibstoff (10% Tankfüllung)", 3500, 3500, 3500, 0, "all", False, True)
tankup = Objekt("Tank-Upgrade", 100000, 100000, 100000, 0, "all", False, True)
ladeup = Objekt("Laderaum-Vergrößerung", 100000, 10000, 10000, 0, "all", False, True)
testing = Objekt("Testing", 0, 0, 0, 0, "all", False, False)
objekte.extend([eisen, h2o, co2, titan, lithium, treibstoffobj, tankup, ladeup, testing])

treibstofftext = "Treibstoff:\n[##########]"

# ----------------------------
# Game logic functions

def Treibstoffaktualisieren():
    global treibstoff, treibstoffmax, treibstofftext
    try:
        geladenerT = treibstoffobj.geladen
    except IndexError:
        geladenerT = 0
    treibstoff = treibstoff + (geladenerT * 10)
    treibstoffobj.geladen = 0
    treibstofftext = "Treibstoff:\n["
    treibstoff_int = int(treibstoff)
    for i in range(1, (treibstoff_int // 10) + 1):
        treibstofftext += "#"
    if (treibstoff_int // 10) < (treibstoffmax // 10):
        zahler = (treibstoffmax // 10) - (treibstoff_int // 10)
        for i in range(zahler + 1):
            treibstofftext += "-"
    treibstofftext += "]"
    if TreibstoffZustand:
        TreibstoffZustand.config(text=treibstofftext)

def DisplayAktualisieren():
    global Geld, Laderaum, sternsystem, Ort, locationImg
    if ListeObjekte:
        ListeObjekte.delete(0, "end")
        for obj in objekte:
            if (obj.stdsystem == "all" or obj.stdsystem == sternsystem) and obj.kaufbar:
                ListeObjekte.insert("end", f"{obj.name} {obj.preis}")
    if ListeLaderaum:
        ListeLaderaum.delete(0, "end")
        ListeLaderaum.insert("end", "Credits: " + str(Geld))
        ListeLaderaum.insert("end", "Platz im Laderaum: " + str(Laderaum))
        ListeLaderaum.insert("end", "------- Geladen:")
        for obj in objekte:
            if (obj.stdsystem == "all" or obj.stdsystem == sternsystem) and obj.verkauflich:
                ListeLaderaum.insert("end", f"{obj.name}: {obj.geladen} Einheiten")
    if ListeOrte:
        ListeOrte.delete(0, "end")
        if sternsystem == sonnensystem:
            for item in sPlaneten:
                name = item.name
                try:
                    if item == Ort:
                        name += "     <----"
                except NameError:
                    pass
                if item.bereisbar:
                    ListeOrte.insert("end", name)
        elif sternsystem == alphacentauri:
            for item in aPlaneten:
                name = item.name
                try:
                    if item == Ort:
                        name += "     <----"
                except NameError:
                    pass
                if item.bereisbar:
                    ListeOrte.insert("end", name)
    if fotolabel:
        fotolabel.config(image=locationImg)

def NeuesSpiel():
    global Geld, Laderaum, treibstoff, sternsystem, Ort, locationImg, game
    testing.geladen = 10000
    Geld = 100000
    Laderaum = 100
    treibstoff = 100
    # Ensure to create PhotoImage with a valid master (game)
    locationImg = tkinter.PhotoImage(master=game, file="./assets/fotos/ship.gif")
    if EingabeMenge:
        EingabeMenge.delete(0, "end")
        EingabeMenge.insert("end", "0")
    sternsystem = sonnensystem
    Ort = sternsystem.startplanet
    DisplayAktualisieren()

def treibstoffkaufen(x):
    treibstoffobj.geladen = x
    Treibstoffaktualisieren()

def upgradekaufen(art, menge):
    global treibstoffmax, Laderaum
    gekauftesobjekt = objekte[art]
    if art == 6:  # Tank-upgrade
        treibstoffmax = (treibstoffmax + 20) * menge
    if art == 7:  # Laderaum-Vergrößerung
        if Laderaum < 130 and menge <= 2:
            addition = 15
        elif Laderaum < 150 and menge <= 2:
            addition = 10
        elif Laderaum >= 150 or menge > 2:
            addition = 5
        Laderaum += addition * menge
    gekauftesobjekt.geladen -= menge

def kaufen():
    global Geld, Laderaum, treibstoff
    try:
        Anzahl = int(EingabeMenge.get())
    except ValueError:
        Anzahl = 0
    try:
        Nummer = int(ListeObjekte.curselection()[0])
    except IndexError:
        try:
            Nummer = int(ListeLaderaum.curselection()[0]) - 3
        except IndexError:
            Nummer = 0
    gekauftesobjekt = objekte[Nummer]
    if cb.get() == 1 and halb.get() == 1:
        messagebox.showinfo("- F E H L E R -", "Du kannst nicht <alles> und <Die Hälfte> auswählen.")
        return
    elif cb.get() == 1: # Checkbox für "alles" ist ausgewählt
        EingabeMenge.delete(0, "end")
        EingabeMenge.insert("end", "0")
        # Anzahl festlegen für alles außer Treibstoff 
        # -> Bei TS wird maximale menge von treibstoffmax geregelt
        if Nummer != 5:
            # ist treibstoff nicht ausgewählt, kann man unendlich viel kaufen (durch Geld beschränkt)
            Anzahl = Geld // gekauftesobjekt.preis
        else: 
            # ist treibstoff ausgewählt, kann man nur so viel kaufen, wie in den Tank passt
            Anzahl = (treibstoffmax - treibstoff) // 10
        if Anzahl > Laderaum:
            Anzahl = Laderaum
    elif halb.get() == 1: # Checkbox für "Die Hälfte" ist ausgewählt
        EingabeMenge.delete(0, "end")
        EingabeMenge.insert("end", "0")
        # Anzahl festlegen für alles außer Treibstoff 
        # -> Bei TS wird maximale menge von treibstoffmax geregelt
        if Nummer != 5:
            # ist treibstoff nicht ausgewählt, kann man unendlich viel kaufen (durch Geld beschränkt)
            Anzahl = (Geld // gekauftesobjekt.preis) // 2
        else:
            # ist treibstoff ausgewählt, kann man nur so viel kaufen, wie in den Tank passt
            Anzahl = ((treibstoffmax - treibstoff) // 10) // 2
        if Anzahl > Laderaum:
            Anzahl = Laderaum
    if Nummer >= 5:
        if Geld >= gekauftesobjekt.preis * Anzahl:
            Geld -= int(gekauftesobjekt.preis) * Anzahl
            gekauftesobjekt.geladen += Anzahl
            if Nummer == 5:
                if treibstoff == treibstoffmax:
                    gekauftesobjekt.geladen -= Anzahl
                    Geld += int(gekauftesobjekt.preis) * Anzahl
                    messagebox.showinfo("- F E H L E R -", "Dein Tank ist bereits voll.\n")
        else:
            messagebox.showinfo("- F E H L E R -", "Du hast zu wenig Geld.\n")
    else:
        if Laderaum >= Anzahl and Geld >= gekauftesobjekt.preis * Anzahl:
            Laderaum -= Anzahl
            Geld -= int(gekauftesobjekt.preis) * Anzahl
            gekauftesobjekt.geladen += Anzahl
        else:
            messagebox.showinfo("- F E H L E R -", "Du hast zu wenig Geld/platz im Laderaum.\n")
    Treibstoffaktualisieren()
    DisplayAktualisieren()

def verkaufen():
    global Geld, Laderaum
    try:
        Anzahl = int(EingabeMenge.get())
    except ValueError:
        Anzahl = 0
    try:
        Nummer = int(ListeLaderaum.curselection()[0]) - 3
        if Nummer < 0:
            Nummer = 8
    except IndexError:
        try:
            Nummer = int(ListeObjekte.curselection()[0])
        except IndexError:
            Nummer = 8
    verkauftesobjekt = objekte[Nummer]
    if cb.get() == 1 and halb.get() == 1:
        messagebox.showinfo("- F E H L E R -", "Du kannst nicht <alles> und <Die Hälfte> auswählen.")
        return
    elif cb.get() == 1:
        EingabeMenge.delete(0, "end")
        EingabeMenge.insert("end", "0")
        Anzahl = verkauftesobjekt.geladen
        if Nummer == 8:
            Anzahl = 0
    elif halb.get() == 1:
        EingabeMenge.delete(0, "end")
        EingabeMenge.insert("end", "0")
        Anzahl = verkauftesobjekt.geladen // 2
        if Nummer == 8:
            Anzahl = 0
    if Anzahl <= verkauftesobjekt.geladen:
        Laderaum += Anzahl
        Geld += int(verkauftesobjekt.preis) * Anzahl
        verkauftesobjekt.geladen -= Anzahl
    else:
        messagebox.showinfo("- F E H L E R -", "Du kannst nicht verkaufen, was du nicht besitzt.\n")
    DisplayAktualisieren()

def warptorcheck():
    global Ort, sternsystem, treibstoff, game
    if Ort.name == "Warptor":
        game.attributes('-alpha', 0)
        warptorfenster = tkinter.Toplevel(game)
        warptorfenster.title("Warptor-Reisen")
        def warperklarung():
            wek = tkinter.Toplevel(game)
            wek.title("Tutorial zum Warptor")
            wektext = (
                "Du hast ein Warptor gefunden! Ein Netz von Warptoren durchsetzt den bewohnten Weltraum.\n"
                "Mit ihnen kannst du schnell von Sternsystem zu Sternsystem reisen. Beachte allerdings, dass diese Reisen nicht billig sind!\n"
                "Du kannst einfach zu einem anderen Planeten in deinem jetzigen Sternsystem reisen, falls du nicht mit dem Warptor reisen willst."
            )
            weklabel = tkinter.Label(wek, text=wektext)
            weklabel.grid(row=1, column=1)
        def warpen():
            global sternsystem, Ort, Geld
            try:
                auswahl = int(sternsystemmenu.curselection()[0])
                auswahl = sternsysteme[auswahl]
            except IndexError:
                auswahl = sternsystem
            if auswahl == sternsystem:
                messagebox.showinfo("- F E H L E R -", "Du kannst nicht in das Sternsystem reisen, in dem du dich befindest.")
            else:
                if Geld < 150000:
                    messagebox.showinfo("- F E H L E R -", "Du hast zu wenig Geld für eine Reise mit dem Warptor.")
                else:
                    sternsystem = auswahl
                    Ort = sternsystem.startplanet
                    DisplayAktualisieren()
                    messagebox.showinfo("- R E I S E I N F O -", "Vielen Dank für die Reise mit Warptor Systems™!\nIn diesem neuen Sternsystem müssen sie auf neue Gefahren achten, aber es gibt auch neue Profitmöglichkeiten...")
                    sleep(3)
                    warptorfenster.destroy()
        preis = tkinter.Label(warptorfenster, text="Festpreis: Eine Reise mit dem Warptor kostet 150000¢")
        preis.grid(row=0, column=1)
        sternsystemmenu = tkinter.Listbox(warptorfenster, width=30, height=5)
        sternsystemmenu.grid(row=1, column=1, padx=5, pady=5)
        sternsystemmenu.delete(0, "end")
        if sternsystem == sonnensystem:
            sternsystemmenu.insert("end", str(sonnensystem.name) + "     <----")
            sternsystemmenu.insert("end", str(alphacentauri.name))
        elif sternsystem == alphacentauri:
            sternsystemmenu.insert("end", str(sonnensystem.name))
            sternsystemmenu.insert("end", str(alphacentauri.name) + "     <----")
        warpen_button = tkinter.Button(warptorfenster, text="Warpen", command=warpen)
        warpen_button.grid(row=2, column=1, pady=5)
        erklarung = tkinter.Button(warptorfenster, text="?", command=warperklarung)
        erklarung.grid(row=3, column=1)
        warptorfenster.protocol("WM_DELETE_WINDOW", lambda: game.attributes('-alpha', 1.0))
    else:
        pass

def weiterfliegen():
    global Ort, treibstoff, reisen, sPlaneten, aPlaneten, sternsystem, Geld, locationImg, Laderaum
    nichtanzeigen = False
    alterplanet = Ort
    if alterplanet.name == "Warptor":
        for widget in warptorhide:
            widget.grid()
    try:
        Nummer = int(ListeOrte.curselection()[0])
    except IndexError:
        Nummer = 0
    try:
        if sternsystem == sonnensystem:
            Ort = sPlaneten[Nummer + 1]
        elif sternsystem == alphacentauri:
            Ort = aPlaneten[Nummer + 1]
    except UnboundLocalError:
        try:
            Ort = Ort
        except NameError:
            if sternsystem == sonnensystem:
                Ort = erde
            elif sternsystem == alphacentauri:
                Ort = alphacentauriab
    ortname = Ort.name
    if ortname == "Warptor":
        for widget in warptorhide:
            widget.grid_remove()
    treibstoffalt = treibstoff
    entfernungalt = alterplanet.koord
    entfernungneu = Ort.koord
    entfernung = abs(entfernungneu - entfernungalt)
    abzug = round(((entfernung / 1500) * 100))
    treibstoff = treibstoff - (treibstoff * (abzug / 100))
    if treibstoff < 0:
        nichtanzeigen = True
        messagebox.showinfo("- A L A R M -", f"Du kannst nicht nach {ortname} reisen.\nDu hast zu wenig Sprit im Tank/einen zu kleinen Tank.\n")
        treibstoff = treibstoffalt
        Ort = alterplanet
    with open("logs.txt", "a+") as logs:
        zeit = datetime.now()
        ts = zeit.strftime("%d.%m;%H:%M")
        writetext = (
            "REISE\n TS: " + ts +
            " Reise " + str(reisen + 1) +
            " planet alt: " + str(alterplanet.name) +
            " planet neu: " + str(Ort.name) +
            " entfernung alt: " + str(entfernungalt) +
            " entfernung neu " + str(entfernungneu) +
            " entfernung ges: " + str(entfernung) +
            " abzug: " + str(abzug) + "\n---------------"
        )
        logs.write(writetext)
        logs.write("\n")
    global zum, zur, zu
    locationImg = Ort.foto
    zum = False
    zur = False
    zu = False
    if ortname in ["Warptor", "Mars", "Pluto"]:
        zum = True
    else:
        zur = True
    if sternsystem == alphacentauri:
        zu = True
        zur = False
        zum = False
    chance = randint(1, 100)
    travelnormal = True
    piraten = False
    alien = False
    wurmloch = False
    if chance > 10 and chance <= 20:
        travelnormal = False
        piraten = True
    elif chance > 20 and chance <= 30:
        travelnormal = False
        alien = True
    elif chance > 30 and chance <= 40:
        travelnormal = False
        wurmloch = True
    benutzbareobjekte = [obj for obj in objekte if obj.verkauflich]
    if travelnormal and not nichtanzeigen:
        if zur and not nichtanzeigen:
            messagebox.showinfo("- R E I S E I N F O -", "Deine Reise geht zur " + ortname + ".\n Sie verläuft ereignislos.\n")
        if zum and not nichtanzeigen:
            messagebox.showinfo("- R E I S E I N F O -", "Deine Reise geht zum " + ortname + ".\n Sie verläuft ereignislos.\n")
        if zu and not nichtanzeigen:
            messagebox.showinfo("- R E I S E I N F O -", "Deine Reise geht zu " + ortname + ".\n Sie verläuft ereignislos.\n")
    elif piraten and not nichtanzeigen:
        if zur:
            messagebox.showinfo("- A L A R M  -", "Auf dem Weg zur " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        if zum:
            messagebox.showinfo("- A L A R M -", "Auf dem Weg zum " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        if zu:
            messagebox.showinfo("- A L A R M -", "Auf dem Weg zu " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        for obj in benutzbareobjekte:
            chance = randint(1, 100)
            if chance > 50:
                diebstahlmenge = obj.geladen // 2
                obj.geladen -= diebstahlmenge
                Laderaum += diebstahlmenge
        Geld = Geld // 2
    elif alien and not nichtanzeigen:
        if sternsystem == alphacentauri:
            if zur:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zur " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\nWer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
            if zum:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zum " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\nWer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
            if zu:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zu " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\nWer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
        elif sternsystem == sonnensystem and not nichtanzeigen:
            if zur:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zur " + ortname + " spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
            if zum:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zum " + ortname + " spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
            if zu:
                messagebox.showinfo("- A L A R M -", "Auf dem Weg zu " + ortname + "  spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
            for obj in benutzbareobjekte:
                chance = randint(1, 100)
                if chance < 75:
                    menge = randint(1, 5)
                    menge = menge * (randint(1, 2) + randint(0, 4))
                    if obj in objekte[:5]:
                        obj.geladen += menge
                        Laderaum -= menge
    elif wurmloch and not nichtanzeigen:
        if zur:
            messagebox.showinfo("- A L A R M -", "Auf dem Weg zur " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\nDu verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        if zum:
            messagebox.showinfo("- A L A R M -", "Auf dem Weg zum " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\nDu verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        if zu:
            messagebox.showinfo("- A L A R M -", "Auf dem Weg zu " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\nDu verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        treibstoff = treibstoff * 0.5
    for obj in objekte:
        obj.preis = randint(obj.preismin, obj.preismax)
    reisen += 1
    DisplayAktualisieren()
    Treibstoffaktualisieren()
    warptorcheck()

def plus():
    try:
        alt = int(EingabeMenge.get())
    except ValueError:
        alt = 0
    EingabeMenge.delete(0, "end")
    neu = alt + 1
    EingabeMenge.insert("end", str(neu))

def minus():
    try:
        alt = int(EingabeMenge.get())
    except ValueError:
        alt = 0
    EingabeMenge.delete(0, "end")
    neu = alt - 1
    if neu < 0:
        neu = 0
    EingabeMenge.insert("end", str(neu))

def hilfe():
    Hilfe = tkinter.Toplevel(game)
    Hilfe.title("Tutorial")
    hilfetext = (
        "Willkommen zu Space Wars!\n"
        "Space Wars ist ein interstellarer Handelssimulator. Dein Ziel ist es, durch geschicktes Kaufen und Verkaufen so viel Gewinn wie möglich zu machen!\n\n"
        "Hier ein kurzes Tutorial:\n"
        "In der Liste oben links findest du die Materialien, die an deinem jetzigen Standort angeboten werden.\n"
        "Du kannst sie durch Anklicken auswählen und durch Klicken auf den gleichnamigen Button kaufen.\n\n"
        "In der Liste oben rechts findest du dein Inventar.\n"
        "Du kannst auch hier durch Anklicken auswählen und mit dem Button 'Verkaufen' verkaufen.\n\n"
        "Unten links findest du eine weitere Liste mit deinen Möglichkeiten zum weiterfliegen.\n"
        "Du kannst durch Klicken auswählen und mit dem Button 'Weiterfliegen' genau dies tun.\n"
        "Mit dem Button 'Neues Spiel' startest du neu,\n"
        "und mit dem Button 'Score hochladen' kannst du deinen Score (dein gesammeltes Geld) mit den 10 besten Spielern vergleichen und hochladen.\n\n"
        "Danke fürs Spielen und viel Spaß!"
    )
    erklaerung = tkinter.Label(Hilfe, text=hilfetext)
    erklaerung.grid(row=1, column=1)

def online():
    global Geld
    score = Geld
    online_win = tkinter.Toplevel(game)
    online_win.title("Score Vergleichen")
    from utils import upload_score
    def hochladen():
        usernameentry = username.get()
        if len(usernameentry.strip()) == 0:
            messagebox.showinfo("- F E H L E R -", "Bitte gib einen Benutzernamen ein, bevor du etwas hochlädst.")
        else:
            upload_score(score, usernameentry)
            scoreaktualisieren()
    scoretext = "Erzielte Punkte: " + str(score)
    scorefeld = tkinter.Label(online_win, text=scoretext)
    scorefeld.grid(row=1, column=3, pady=5)
    username = tkinter.Entry(online_win)
    username.grid(row=3, column=3)
    usernamelabel = tkinter.Label(online_win, text="Benutzername:")
    usernamelabel.grid(row=3, column=2)
    upload_btn = tkinter.Button(online_win, text="Score hochladen", command=hochladen)
    upload_btn.grid(row=4, column=3, pady=5)
    spacer2 = tkinter.Label(online_win, text="|")
    spacer2.grid(row=1, column=1)
    spacer3 = tkinter.Label(online_win, text="|")
    spacer3.grid(row=2, column=1)
    spacer4 = tkinter.Label(online_win, text="|")
    spacer4.grid(row=3, column=1)
    spacer5 = tkinter.Label(online_win, text="|")
    spacer5.grid(row=4, column=1)
    highscoreslabel = tkinter.Label(online_win, text="Noch keine Scores vorhanden")
    highscoreslabel.grid(row=1, column=0)
    def scoreaktualisieren():
        import csv
        daten = []
        kategorien = []
        try:
            with open("score.csv", "r") as p:
                reader = csv.reader(p)
                kategorien = next(reader)
                for row in reader:
                    daten.append(row)
            ganzeliste = []
            for row in daten:
                ganzeliste.append({kategorien[1]: int(row[1]), kategorien[0]: row[0]})
            sortiert = sorted(ganzeliste, key=lambda item: item.get("Score"), reverse=True)
            sortiert = sortiert[:10]
            highscorestext = ""
            for entry in sortiert:
                highscorestext += "\n" + str(entry["Benutzername"]) + " : " + str(entry["Score"])
            highscoreslabel.config(text=highscorestext)
        except FileNotFoundError:
            pass
    scoreaktualisieren()

def closinglog():
    from utils import write_closing_log
    write_closing_log(Geld, reisen)