import tkinter
# tankmodifikator durch upgrades (für py) <- keine ahnung warum das da steht, vielleicht hab ich was kaputt gemacht

def kaufen(geld, objekt, menge, alles, halb):
    from game import treibstoffzustand, eingabemenge, displayaktualisieren
    from objects import treibstoffobj, allupgrades
    from settings import TEXT_BOTH_BUY_BUTTONS, TEXT_NO_MONEY, MAX_TREIBSTOFF, treibstoff, laderaum
    from treibstoff import treibstoffaktualiseren
    # verknüpfen der übergebenen variablen "menge" & "geld" mit den zu verwendenden
    menge = menge
    geld = geld
    # falls sowohl der button "alles kaufen" 
    # als auch der button "die hälfte kaufen" ausgewählt sind
    if alles and halb:
        tkinter.messagebox.showinfo(TEXT_BOTH_BUY_BUTTONS)
    # falls "alles" ausgewählt ist
    if alles:
        eingabemenge.delete("0","end")
        eingabemenge.insert("end","0")
        menge = geld//objekt.preis
        if menge > laderaum:
            menge = laderaum
    # falls "die hälfte" ausgewählt ist
    elif halb:
        eingabemenge.delete("0","end")
        eingabemenge.insert("end","0")
        menge = (geld//objekt.preis)//2
        if menge > laderaum:
            menge = laderaum
    # eigener kaufvorgang bei Treibstoff und Upgrades
    if objekt.name == treibstoffobj.name or objekt in allupgrades:
        # objekt kaufen, falls genügend geld vorhanden
        if (geld >= objekt.preis*menge):
            geld -= int(objekt.preis)*menge
            objekt.geladen += menge
            # kaufvorgang für treibstoff
            if objekt.name == treibstoffobj.name:
                # wenn der tank schon voll ist, geld+laderaum zurückerstatten
                if treibstoff >= MAX_TREIBSTOFF:
                    objekt.geladen -= menge
                    geld += int(objekt.preis)*menge
                    tkinter.messagebox.showinfo("- F E H L E R -","Dein Tank ist bereits voll.\n")
                else:
                    # wenn platz im tank ist, kaufvorgang initiieren
                    treibstoffaktualiseren(treibstoffzustand)
            else:
                # wenn ein upgrade gekauft wird, kaufvorgang initiieren
                upgradekaufen(objekt, menge)
        else:
            # wenn zu wenig geld vorhanden ist, wird nicht gekauft
            tkinter.messagebox.showinfo(TEXT_NO_MONEY)
    else:
        # "normaler" kaufvorgang wenn kein upgrade/treibstoff gekauft wird
        if (laderaum >= menge) and (geld >= objekt.preis*menge):
            laderaum -= menge
            geld -= int(objekt.preis)*menge
            objekt.geladen += menge
        else:
            tkinter.messagebox.showinfo("- F E H L E R -","Du hast zu wenig geld/Platz im laderaum.\n")
    # TODO: logs
    # display mit neuen werten aktualisieren
    displayaktualisieren()
        
def upgradekaufen(objekt, menge):
    from objects import tankup, ladeup
    # muss hardcoded für jedes upgrade sein :(
    #tank-upgrade
    if objekt == tankup:
        global tankmodifier
        tankmodifier += 20*menge
    #laderaum-upgrade
    if objekt == ladeup:
        # nach und nach kleiner werdende zunahme bei upgrades
        if laderaum<130 and menge<=2:
            addition = 15
        elif laderaum<150 and menge<=2:
            addition = 10
        elif laderaum>=150 or menge>2:
            addition = 5
        laderaum += addition*menge
    # entfernen von upgrades, damit man keinen laderaumplatz verliert 
    # & damit upgrades nicht öfter wirken
    objekt.geladen -= menge

def verkaufen(geld, objekt, menge, alles, halb):
    from settings import TEXT_BOTH_BUY_BUTTONS
    from game import displayaktualisieren, eingabemenge
    # verknüpfen der übergebenen variablen "menge" & "geld" mit den zu verwendenden
    menge = menge
    # falls sowohl der button "alles kaufen" 
    # als auch der button "die hälfte kaufen" ausgewählt sind
    if alles and halb:
        tkinter.messagebox.showinfo(TEXT_BOTH_BUY_BUTTONS)
    # falls "alles" ausgewählt ist
    if alles:
        eingabemenge.delete("0","end")
        eingabemenge.insert("end","0")
        menge = objekt.geladen
    # falls "die hälfte" ausgewählt ist
    elif halb:
        eingabemenge.delete("0","end")
        eingabemenge.insert("end","0")
        menge = objekt.geladen // 2
    # eigentlicher verkaufvorgang
    if (menge <= objekt.geladen):
        Laderaum = Laderaum + menge
        geld = geld + int(objekt.preis)*menge
        objekt.geladen = objekt.geladen - menge
    else:
        tkinter.messagebox.showinfo("- F E H L E R -","Du kannst nicht verkaufen, was du nicht besitzt.\n")
    # TODO: logs
    # display mit neuen werten aktualisieren
    displayaktualisieren()