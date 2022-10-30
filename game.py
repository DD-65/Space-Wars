import tkinter
global fenster
fenster = tkinter.Tk()
fenster.title("Space Wars")

# TODO: get game to work as intended :D

## TODO: je nach bedarf variablen hinzufügen, die während dem spielverlauf geändert werden
## TODO: ein zeit-system (etwa ein tick pro km flug) und darauf aufbauend ein wirtschafts-system hinzufügen

def displayaktualisieren():
    from settings import geld, laderaum
    from objects import objekte
    from travel import standortplanet, standortsystem
    from planets import sonnensystem, splaneten, alphacentauri, aplaneten
    #from gui import  listeobjekte, listeladeraum, listeorte, fotolabel
    # OBJEKTE ANZEIGEN
    listeobjekte.delete("0","end")
    for i in range(0,len(objekte)):
        if (objekte[i].stdsystem=="all" or objekte[i].stdsystem==standortsystem) and objekte[i].kaufbar==True:
            listeobjekte.insert("end",objekte[i].name+ " "+ str(objekte[i].preis))
    
    # ladung anzeigen
    listeladeraum.delete("0","end")
    listeladeraum.insert("end", "Credits: " + str(geld))
    listeladeraum.insert("end", "Platz im Laderaum: " + str(laderaum))
    listeladeraum.insert("end", "------- Geladen:")
    for i in range(0, len(objekte)):
        if (objekte[i].stdsystem=="all" or objekte[i].stdsystem==standortsystem) and objekte[i].verkauflich==True:
            listeladeraum.insert("end",objekte[i].name+ ": "+ str(objekte[i].geladen)+" Einheiten")
    
    # orte anzeigen
    listeorte.delete("0","end")
    # Nur die planeten des jeweiligen sonnensystems in der gui anzeigen + indikator
    if standortsystem==sonnensystem:
        for i in range(0,len(splaneten)):
            item=splaneten[i]
            name=item.name
            # Indikator an welchem Planeten man gerade ist
            try:
                if item==standortplanet:
                    name=name+"     <----"
            except NameError:
                pass
            # NUR DIE BEREISBAREN PLANETEN IN DER LISTE ANZEIGEN
            if item.bereisbar==True:
                listeorte.insert("end",name)
            else:
                pass
    elif standortsystem==alphacentauri:
        for i in range(0,len(aplaneten)):
            item=aplaneten[i]
            name=item.name
            # Indikator an welchem Planeten man gerade ist
            try:
                if item==standortplanet:
                    name=name+"     <----"
            except NameError:
                pass
            # NUR DIE BEREISBAREN PLANETEN IN DER LISTE ANZEIGEN
            if item.bereisbar==True:
                listeorte.insert("end",name)
            else:
                pass
    global locationImg
    fotolabel.configure(image=locationImg)

# TODO: warptor etc
def kaufen():
    from settings import geld
    from objects import objekte
    from trading import kaufen as k
    #from gui import  eingabemenge, listeladeraum, listeobjekte, cb, halb
    try:
        Anzahl = int(eingabemenge.get())
    except ValueError: # FALLS NICHTS EINGEGEBEN IST ( BEI ZU KAUFENDER MENGE)
        Anzahl=0
    try:
        Nummer = int(listeobjekte.curselection()[0])
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST (BEIM ZU KAUFENDEN OBJEKT)
        try:
            Nummer = (int(listeladeraum.curselection()[0]))-3 # falls auf der falschen liste ausgewählt wurde
        except IndexError:
            Nummer=0
    gekauftesobjekt=objekte[Nummer]
    alles = cb.get() == 1
    haelfte = halb.get() == 1
    k(geld, gekauftesobjekt, Anzahl, alles, haelfte)

def verkaufen():
    from objects import objekte
    from settings import geld
    from trading import verkaufen as v
    #from gui import  eingabemenge, listeladeraum, listeobjekte, cb, halb
    try:
        Anzahl = int(eingabemenge.get())
    except ValueError: # FALLS NICHTS EINGEGEBEN IST (BEI DER ZU  VERKAUFENDEN MENGE)
        Anzahl=0
    try:
        Nummer = int(listeladeraum.curselection()[0])-3
        # wenn nummer<0 ist, d.h. eines der nicht verkaufbaren objekte ausgewählt ist, wird nummer auf 9 gesetzt; das entspricht einem objekt ohne wert
        if Nummer<0:
            Nummer=8
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST ( BEI ZU VERKAUFENDEM OBJEKT)
        try:
            Nummer = int(listeobjekte.curselection()[0]) # falls auf anderer liste ausgewählt wurde
        except IndexError:
            Nummer=8
    verkauftesobjekt=objekte[Nummer]
    alles = cb.get() == 1
    haelfte = halb.get() == 1
    v(geld, verkauftesobjekt, Anzahl, alles, haelfte)

def plus():
    #from gui import  eingabemenge
    try:
        alt=int(eingabemenge.get())
    except ValueError:
        alt = 0
    eingabemenge.delete("0","end")
    neu=alt+1
    eingabemenge.insert("end",str(neu))

def minus():
    #from gui import  eingabemenge
    try:
        alt=int(eingabemenge.get())
    except ValueError:
        alt = 0
    eingabemenge.delete("0","end")
    neu=alt-1
    if neu<0:
        neu=0
    eingabemenge.insert("end",str(neu))

def weiterfliegen():
    from travel import standortsystem, standortplanet
    #from gui import  listeorte
    alterplanet = standortplanet
    try:
        Nummer = int(listeorte.curselection()[0])
        neuerplanet = standortsystem.planeten[Nummer+1]
        weiterfliegen(neuerplanet, alterplanet)
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST (BEI FLUGZIEL)
        pass

def neuesspiel():
    from settings import STARTGELD, STARTLADERAUM, STARTPLANET, STARTSTERNSYSTEM
    #from gui import  eingabemenge
    global tankmodifier
    geld = STARTGELD
    laderaum = STARTLADERAUM
    tankmodifier = 0
    locationImg=tkinter.PhotoImage(file="./assets/fotos/ship.gif")
    eingabemenge.delete("0","end")
    eingabemenge.insert("end","0")
    standortsystem = STARTSTERNSYSTEM
    standortplanet = STARTPLANET
    displayaktualisieren()

def hilfe():
    from settings import TEXT_TUTORIAL
    hilfe=tkinter.Toplevel()
    hilfe.title("Tutorial")
    hilfetext = TEXT_TUTORIAL
    erklaerung=tkinter.Label(hilfe,text=hilfetext)
    erklaerung.grid(row=1,column=1)

def online():
    print("in development :D")
    #TODO: online services

global listeobjekte
listeobjekte = tkinter.Listbox (width=30, height = 10)
listeobjekte.grid(padx = 5, pady = 5, row = 1, column = 1, columnspan = 1, rowspan=4)

labelmenge = tkinter.Label(fenster, text = 'Menge: ')
labelmenge.grid (row = 1, column = 2)

buttonplus=tkinter.Button(fenster,text="+",command=plus)
buttonplus.grid(row=1,column=3)

buttonminus=tkinter.Button(fenster,text="-",command=minus)
buttonminus.grid(row=1,column=5)

eingabemenge = tkinter.Entry(fenster, width = 4)
eingabemenge.grid(row = 1, column = 4)

cb=tkinter.IntVar()
buttonalles = tkinter.Checkbutton(fenster,text="Alles",variable=cb)
buttonalles.grid(row=3,column=2,padx=5)

halb=tkinter.IntVar()
buttonhalfte=tkinter.Checkbutton(fenster,text="Die Hälfte",variable=halb)
buttonhalfte.grid(row=3,column=3,padx=5)

buttonkaufen = tkinter.Button(fenster, text=' Kaufen  >>> ', command = kaufen)
buttonkaufen.grid(padx=5, row =2, column = 2, columnspan=2)

buttonverkaufen = tkinter.Button(fenster, text=' <<< Verkaufen ', command = verkaufen)
buttonverkaufen.grid(padx=5, row =4, column = 2, columnspan=2)

listeladeraum = tkinter.Listbox (width=30, height = 10)
listeladeraum.grid(padx = 5, pady = 5, row = 1, column = 6, columnspan = 2, rowspan=4)
#-----------------------
listeorte = tkinter.Listbox (width=30, height = 6)
listeorte.grid(padx = 5, pady = 20, row = 5, column = 1, columnspan = 1, rowspan=4)

buttonbewegen = tkinter.Button(fenster, text = ' Weiterfliegen.. ', command = weiterfliegen)
buttonbewegen.grid(row=7, column=2, padx=5, columnspan = 2)

buttonneustart = tkinter.Button(fenster, text = ' Neues Spiel ', command = neuesspiel)
buttonneustart.grid(row=6, column=6, padx=5, pady=25)

hilfebutton=tkinter.Button(fenster,text="Tutorial",command=hilfe)
hilfebutton.grid(row=8,column=6,pady=5,padx=5)

buttononline=tkinter.Button(fenster,text="Score hochladen",command=online)
buttononline.grid(row=7,column=6,padx=5,pady=5)
#-----------------------
treibstofftext="Treibstoff:\n[##########]"
global treibstoffzustand
treibstoffzustand=tkinter.Label(fenster,text=treibstofftext)
treibstoffzustand.grid(row=8,column=2,padx=5, columnspan=2)
# ---------------------
global locationImg
locationImg=tkinter.PhotoImage(file="./assets/fotos/ship.gif")
global fotolabel
fotolabel=tkinter.Label(image=locationImg)
fotolabel.grid(row=1,column=0,rowspan=8) 

#liste an widgets die versteckt werden sollen falls man zum warptor gelangt
warptorhide=[listeladeraum, listeobjekte, buttonalles, buttonhalfte, buttonkaufen, buttonverkaufen, labelmenge, buttonplus, buttonminus, eingabemenge]

if __name__ == "__main__":
    # on startup: gui aktualisieren
    displayaktualisieren()

# loop
try:
    fenster.mainloop()
except KeyboardInterrupt:
    pass
