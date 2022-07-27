import tkinter, csv
from random import *
from datetime import datetime
from tkinter import messagebox
from typing import List
from time import sleep
#Fensterdefinition jetzt schon um Bilder mit PhotoImage definieren zu können
game = tkinter.Tk()
game.title("Space Wars")
Geld = 10000 # STARTGELD DES SPIELERS
Laderaum = 100 # FREIER LADERAUM IM SCHIFF DES SPIELERS (AM ANFANG)
global reisen
reisen=0 # ANZAHL DER REISEN VON PLANET ZU PLANET
galaxienreisen=0 # ANZAHL DER REISEN ZWISCHEN GALAXIEN (WARPTOR)
treibstoff=100 # TREIBSTOFFFÜLLUNG
treibstoffmax=100
erstereise=True


# PLANETEN
class planet:
    def __init__(self,name,sonnensystem,koord,warptor,bereisbar,foto):
        self.name=name
        self.sonnensystem=sonnensystem
        self.koord=koord
        self.warptor=warptor
        self.bereisbar=bereisbar
        self.foto=foto

# PLANETENDEFINITION
# PLANETEN DES SONNENSYSTEMS

planeten=[]
#BEISPIEL:                     ENTFERNUNG   BEREISBAR T/F
#BEISPIEL:   NAME  PLANETENSYSTEM    WARPTOR T/F    BILD
sonne=planet("Sonne","Milchstraße",0,False,False,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
erde=planet("Erde","Milchstraße",250,False,True,tkinter.PhotoImage(file="./assets/fotos/erde.gif"))
mars=planet("Mars","Milchstraße",370,False,True,tkinter.PhotoImage(file="./assets/fotos/mars.gif"))
venus=planet("Venus-Raumstation","Milchstraße",100,False,True,tkinter.PhotoImage(file="./assets/fotos/venus.gif"))
uranus=planet("Uranus-Raumstation","Milchstraße",600,False,True,tkinter.PhotoImage(file="./assets/fotos/uranus.gif"))
pluto=planet("Pluto","Milchstraße",1100,False,True,tkinter.PhotoImage(file="./assets/fotos/pluto.gif"))
warptorS=planet("Warptor","Milchstraße",1000,True,True,tkinter.PhotoImage(file="./assets/fotos/warp.gif"))
# PLANETEN VON ALPHA CENTAURI
alphacentauria=planet("Alpha Centauri A (Stern)","Alpha Centauri",0,False,False,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
alphacentauriab=planet("Alpha Centauri Ab","Alpha Centauri",150,False,True,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
alphacentauribb=planet("Alpha Centauri Bb","Alpha Centauri",2580,False,True,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
warptorA=planet("Warptor","Alpha Centauri",1000,True,True,tkinter.PhotoImage(file="./assets/fotos/warp.gif"))

sPlaneten= [sonne,erde,mars,venus,uranus,pluto,warptorS] # PLANETEN DES SONNENSYSTEMS
aPlaneten=[alphacentauria,alphacentauriab,alphacentauribb,warptorA] # PLANETEN UM ALPHA CENTAURI
planeten=planeten+aPlaneten+sPlaneten

sternsysteme=[]
class Planetensystem:
    def __init__(self, name, planeten,startplanet):
        self.name=name
        self.planeten=planeten
        self.startplanet=startplanet
sonnensystem=Planetensystem("Sonnensystem",sPlaneten, erde)
alphacentauri=Planetensystem("Alpha Centauri",aPlaneten, alphacentauria)
sternsysteme=sternsysteme+[sonnensystem,alphacentauri]

sternsystem=sonnensystem # AKTUELLES STERNSYSTEM

global Ort # Startplaneten für jedes sternsystem festlegen
Ort=sternsystem.startplanet

class Objekt:
    def __init__(self, name, preis, preismax, preismin, geladen, stdsystem, verkauflich,kaufbar):
        self.name=name
        self.preis=preis
        self.preismax=preismax
        self.preismin=preismin
        self.geladen=geladen
        self.stdsystem=stdsystem
        self.verkauflich=verkauflich
        self.kaufbar=kaufbar

# Objektdefinition
#reihenfolge:name,preis,preismax,preismin,geladen,sonnensystem (in welchem das objekt kaufbar ist), verkauflich (ob das Objekt verkauft werden kann), kaufbar(ob das Objekt kaufbar ist)
objekte=[]
eisen=Objekt("Eisen",250,1350,100,0,sonnensystem,True,True)
h2o=Objekt("H2O",750,1700,200,0,sonnensystem,True,True)
co2=Objekt("CO2",600,2000,200,0,sonnensystem,True,True)
titan=Objekt("Titan",380,1800,150,0,sonnensystem,True,True)
lithium=Objekt("Lithium",1000,7500,400,0,sonnensystem,True,True)
treibstoffobj=Objekt("Treibstoff (10% Tankfüllung)",3500,3500,3500,0,"all",False,True)
tankup=Objekt("Tank-Upgrade",100000,100000,100000,0,"all",False,True)
ladeup=Objekt("Laderaum-Vergrößerung",100000,10000,10000,0,"all",False,True)
testing=Objekt("Testing",0,0,0,0,"all",False,False)
objekte=objekte+[eisen,h2o,co2,titan,lithium,treibstoffobj,tankup,ladeup,testing]

# TREIBSTOFFF
treibstofftext="Treibstoff:\n[##########]"
def Treibstoffaktualisieren():
    global treibstofftext
    global treibstoff
    global treibstoffmax
    try:
        geladenerT=treibstoffobj.geladen
    except IndexError: # FALLS KEIN TREIBSTOFF GELADEN
        geladenerT=0
    treibstoff=treibstoff+(geladenerT*10)
    treibstoffobj.geladen=0
    treibstofftext="Treibstoff:\n"+"["
    treibstoff=int(treibstoff)
    for i in range(1,(treibstoff//10)+1): # PRO 10% DES TREIBSTOFFS EIN STRICH IN DER GUI
        treibstofftext=treibstofftext+"#"
    if (treibstoff//10)<(treibstoffmax//10):
        zahler=(treibstoffmax//10)-(treibstoff//10)
        for i in range(0,zahler+1):
            treibstofftext=treibstofftext+"-"
    treibstofftext=treibstofftext+"]"
    TreibstoffZustand["text"]=treibstofftext

def DisplayAktualisieren():
    global Geld
    global Laderaum, sternsystem

    # OBJEKTE ANZEIGEN
    ListeObjekte.delete("0","end")
    for i in range(0,len(objekte)):
        if (objekte[i].stdsystem=="all" or objekte[i].stdsystem==sternsystem) and objekte[i].kaufbar==True:
            ListeObjekte.insert("end",objekte[i].name+ " "+ str(objekte[i].preis))
    
    # ladung anzeigen
    ListeLaderaum.delete("0","end")
    ListeLaderaum.insert("end", "Credits: " + str(Geld))
    ListeLaderaum.insert("end", "Platz im Laderaum: " + str(Laderaum))
    ListeLaderaum.insert("end", "------- Geladen:")
    for i in range(0, len(objekte)):
        if (objekte[i].stdsystem=="all" or objekte[i].stdsystem==sternsystem) and objekte[i].verkauflich==True:
            ListeLaderaum.insert("end",objekte[i].name+ ": "+ str(objekte[i].geladen)+" Einheiten")
    
    # orte anzeigen
    ListeOrte.delete("0","end")
    # Nur die planeten des jeweiligen sonnensystems in der gui anzeigen + indikator
    if sternsystem==sonnensystem:
        for i in range(0,len(sPlaneten)):
            item=sPlaneten[i]
            name=item.name
            # Indikator an welchem Planeten man gerade ist
            try:
                if item==Ort:
                    name=name+"     <----"
            except NameError:
                pass
            # NUR DIE BEREISBAREN PLANETEN IN DER LISTE ANZEIGEN
            if item.bereisbar==True:
                ListeOrte.insert("end",name)
            else:
                pass
    elif sternsystem==alphacentauri:
        for i in range(0,len(aPlaneten)):
            item=aPlaneten[i]
            name=item.name
            # Indikator an welchem Planeten man gerade ist
            try:
                if item==Ort:
                    name=name+"     <----"
            except NameError:
                pass
            # NUR DIE BEREISBAREN PLANETEN IN DER LISTE ANZEIGEN
            if item.bereisbar==True:
                ListeOrte.insert("end",name)
            else:
                pass
    global locationImg
    fotolabel.configure(image=locationImg)

def NeuesSpiel():
    global Geld
    global Laderaum
    global treibstoff
    global EingabeMenge
    global sternsystem
    testing.geladen=10000
    Geld = 100000
    Laderaum = 100
    treibstoff=100
    global locationImg
    locationImg=tkinter.PhotoImage(file="./assets/fotos/ship.gif")
    EingabeMenge.delete("0","end")
    EingabeMenge.insert("end","0")
    sternsystem=sonnensystem
    DisplayAktualisieren()

def treibstoffkaufen(x):
    global geladenerT
    geladenerT=x
    Treibstoffaktualisieren()

def upgradekaufen(art,menge):
    gekauftesobjekt=objekte[art]
    if art==6: # wenn Tank-upgrade ausgewählt wurde
        global treibstoffmax
        treibstoffmax=(treibstoffmax+20)*menge
    if art==7: #wenn laderaumupgrade ausgewält wurde
        global Laderaum
        # nach und nach kleiner werdende zunahme bei upgrades
        if Laderaum<130 and menge<=2:
            addition=15
        elif Laderaum<150 and menge<=2:
            addition=10
        elif Laderaum>=150 or menge>2:
            addition=5
        Laderaum=Laderaum+(addition)*menge
    gekauftesobjekt.geladen=gekauftesobjekt.geladen-menge
 
def kaufen():
    global Geld
    global Laderaum
    global treibstoff
    global treibstoffmax
    ladealt=Laderaum
    geldalt=Geld
    try:
        Anzahl = int(EingabeMenge.get())
    except ValueError: # FALLS NICHTS EINGEGEBEN IST ( BEI ZU KAUFENDER MENGE)
        Anzahl=0
    try:
        Nummer = int(ListeObjekte.curselection()[0])
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST (BEIM ZU KAUFENDEN OBJEKT)
        try:
            Nummer = (int(ListeLaderaum.curselection()[0]))-3 # falls auf der falschen liste ausgewählt wurde
        except IndexError:
            Nummer=0
    gekauftesobjekt=objekte[Nummer]
    # Falls "alles" und "hälfte" ausgewählt sind
    if cb.get()==1 and halb.get()==1:
        tkinter.messagebox.showinfo("- F E H L E R -","Du kannst nicht <alles> und <Die Hälfte> auswählen.")
    # Falls "alles" (der button) ausgewählt ist
    elif cb.get()==1:
        EingabeMenge.delete("0","end")
        EingabeMenge.insert("end","0")
        Anzahl=Geld//gekauftesobjekt.preis
        if Anzahl>Laderaum:
            Anzahl=Laderaum
    # Falls "die hälfte" ausgewählt ist
    elif halb.get()==1:
        EingabeMenge.delete("0","end")
        EingabeMenge.insert("end","0")
        Anzahl=(Geld//gekauftesobjekt.preis)//2
        if Anzahl>Laderaum:
            Anzahl=Laderaum
    # EIgener Kaufvorgang bei Treibstoff und Upgrades
    if Nummer>=5:
        if (Geld >= gekauftesobjekt.preis*Anzahl):
            Geld = Geld - int(gekauftesobjekt.preis)*Anzahl
            gekauftesobjekt.geladen=gekauftesobjekt.geladen+Anzahl
            if Nummer==5:
                if treibstoff==treibstoffmax:
                    gekauftesobjekt.geladen=gekauftesobjekt.geladen-Anzahl
                    Geld = Geld + int(gekauftesobjekt.preis)*Anzahl
                    tkinter.messagebox.showinfo("- F E H L E R -","Dein Tank ist bereits voll.\n")
            else:
                upgradekaufen(Nummer,Anzahl)
        else:
            tkinter.messagebox.showinfo("- F E H L E R -","Du hast zu wenig Geld.\n")
    else:
        if (Laderaum >= Anzahl) and (Geld >= gekauftesobjekt.preis*Anzahl):
            Laderaum = Laderaum - Anzahl
            Geld = Geld - int(gekauftesobjekt.preis)*Anzahl
            gekauftesobjekt.geladen = gekauftesobjekt.geladen+Anzahl
        else:
            tkinter.messagebox.showinfo("- F E H L E R -","Du hast zu wenig Geld/platz im Laderaum.\n")
    Treibstoffaktualisieren()
    geldneu=Geld
    # logs
    # vermeiden dass bei drücken des buttons ohne kauf ein logeintrag angelegt wird (gleiches bei verkaufen())
    #if (geldalt<geldneu):
    #    with open("logs.txt", "a+") as logs:
    #        zeit=datetime.now()
    #        ts=zeit.strftime("%d.%m;%H:%M")
    #        writetext="KAUF\n"+" TS: "+ts+" Ladeplatz alt: "+str(ladealt)+" Ladeplatz neu: "+str(ladeneu)+ " Geld alt: "+str(geldalt)+" Geld neu: "+str(geldneu)+"\n"+"Geladen alt:\n"+"Eisen: "+str(geladenalt[1])+"\n"+"H2O: "+str(geladenalt[2])+"\n"+"CO2: "+str(geladenalt[3])+"\n"+"Titan: "+str(geladenalt[4])+"\n"+"Lithium: "+str(geladenalt[5])+"\n"+"Geladen neu:\n"+"Eisen: "+str(geladenneu[1])+"\n"+"H2O: "+str(geladenneu[2])+"\n"+"CO2: "+str(geladenneu[3])+"\n"+"Titan: "+str(geladenneu[4])+"\n"+"Lithium: "+str(geladenneu[5])+"\n"+"\n---------------"
    #        logs.write(writetext)
    #        logs.write("\n")
    DisplayAktualisieren()

def verkaufen():
    global Geld
    global ListeLaderaum
    global Laderaum
    ladealt=Laderaum
    geldalt=Geld
    try:
        Anzahl = int(EingabeMenge.get())
    except ValueError: # FALLS NICHTS EINGEGEBEN IST (BEI DER ZU  VERKAUFENDEN MENGE)
        Anzahl=0
    try:
        Nummer = int(ListeLaderaum.curselection()[0])-3
        # wenn nummer<0 ist, d.h. eines der nicht verkaufbaren objekte ausgewählt ist, wird nummer auf 9 gesetzt; das entspricht einem objekt ohne wert
        if Nummer<0:
            Nummer=8
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST ( BEI ZU VERKAUFENDEM OBJEKT)
        try:
            Nummer = int(ListeObjekte.curselection()[0]) # falls auf anderer liste ausgewählt wurde
        except IndexError:
            Nummer=8
    verkauftesobjekt=objekte[Nummer]
    # Falls "alles" und "hälfte" ausgewählt sind
    if cb.get()==1 and halb.get()==1:
        tkinter.messagebox.showinfo("- F E H L E R -","Du kannst nicht <alles> und <Die Hälfte> auswählen.")
    # falls "alles" (button) ausgewählt ist
    elif cb.get()==1:
        EingabeMenge.delete("0","end")
        EingabeMenge.insert("end","0")
        Anzahl=verkauftesobjekt.geladen
        #wenn "debug-"item ausgewählt ist (nummer 8) -> es soll nicht gekauft werden
        if Nummer==8:
            Anzahl=0
    # wenn "halb" ausgewählt ist
    elif halb.get()==1:
        EingabeMenge.delete("0","end")
        EingabeMenge.insert("end","0")
        Anzahl=verkauftesobjekt.geladen//2
        # wenn debug-item ausgewählt ist, wird anzahl auf 0 gesetzt, damit man keine laderaumplätze ercheaten kann
        if Nummer==8:
            Anzahl=0
    if (Anzahl <= verkauftesobjekt.geladen):
        Laderaum = Laderaum + Anzahl
        Geld = Geld + int(verkauftesobjekt.preis)*Anzahl
        verkauftesobjekt.geladen = verkauftesobjekt.geladen - Anzahl
    else:
        tkinter.messagebox.showinfo("- F E H L E R -","Du kannst nicht verkaufen, was du nicht besitzt.\n")
    geldneu=Geld
    ladeneu=Laderaum
    # logs
    #if (geladenalt[1]+geladenalt[2]+geladenalt[3]+geladenalt[4]+geladenalt[5])>(geladenneu[1]+geladenneu[2]+geladenneu[3]+geladenneu[4]+geladenneu[5]):
    #    with open("logs.txt", "a+") as logs:
    #        zeit=datetime.now()
    #        ts=zeit.strftime("%d.%m;%H:%M")
    #        writetext="KAUF\n"+" TS: "+ts+" Ladeplatz alt: "+str(ladealt)+" Ladeplatz neu: "+str(ladeneu)+ " Geld alt: "+str(geldalt)+" Geld neu: "+str(geldneu)+"\n"+"Geladen alt:\n"+"Eisen: "+str(geladenalt[1])+"\n"+"H2O: "+str(geladenalt[2])+"\n"+"CO2: "+str(geladenalt[3])+"\n"+"Titan: "+str(geladenalt[4])+"\n"+"Lithium: "+str(geladenalt[5])+"\n"+"Geladen neu:\n"+"Eisen: "+str(geladenneu[1])+"\n"+"H2O: "+str(geladenneu[2])+"\n"+"CO2: "+str(geladenneu[3])+"\n"+"Titan: "+str(geladenneu[4])+"\n"+"Lithium: "+str(geladenneu[5])+"\n"+"\n---------------"
    #        logs.write(writetext)
    #        logs.write("\n")
    DisplayAktualisieren()

def warptorcheck():
    global Ort
    global aPlaneten
    global sPlaneten
    global treibstoff
    global sternsystem, sternsysteme

    if Ort.name=="Warptor":
        game.attributes('-alpha', 0)
        global warptorfenster
        warptorfenster=tkinter.Toplevel()
        warptorfenster.title("Warptor-Reisen")

        def warperklarung():
            wek=tkinter.Toplevel()
            wek.title("Tutorial zum Warptor")
            wektext="""Du hast ein Warptor gefunden! Ein Netz von Warptoren durchsetzt den bewohnten Weltraum.
            Mit ihnen kannst du schnell von Sternsystem zu Sternsystem reisen. Beachte allerdings, dass diese Reisen nicht billig sind!
            Du kannst einfach zu einem anderen Planeten in deinem jetzigen Sternsystem reisen, falls du nicht mit dem Warptor reisen willst.
            """
            weklabel=tkinter.Label(wek, text=wektext)
            weklabel.grid(row=1,column=1)

        
        def warpen():
            global sternsystem, sternsysteme, Ort, Geld
            try:
                auswahl=int(sternsystemmenu.curselection()[0])
                auswahl=sternsysteme[auswahl]
            except IndexError:
                auswahl=sternsystem
            if auswahl==sternsystem:
                tkinter.messagebox.showinfo("- F E H L E R -","Du kannst nicht in das Sternsystem reisen, in dem du dich befindest.")
            else:
                if Geld<150000:
                    tkinter.messagebox.showinfo("- F E H L E R -","Du hast zu wenig Geld für eine Reise mit dem Warptor.")
                else:
                    sternsystem=auswahl
                    Ort=sternsystem.startplanet
                    DisplayAktualisieren()
                    tkinter.messagebox.showinfo("- R E I S E I N F O -","Vielen Dank für die Reise mit Warptor Systems™!\nIn diesem neuen Sternsystem müssen sie auf neue Gefahren achten, aber es gibt auch neue Profitmöglichkeiten...")                    
                    sleep(3)
                    warptorfenster.destroy
            
        preis=tkinter.Label(warptorfenster,text="Festpreis: Eine Reise mit dem Warptor kostet 150000¢")
        preis.grid(row=0,column=1)

        sternsystemmenu=tkinter.Listbox(warptorfenster, width=30, height=5)
        sternsystemmenu.grid(row=1,column=1, padx=5, pady=5)

        sternsystemmenu.delete("0","end")
        if sternsystem==sonnensystem:
            sternsystemmenu.insert("end",str(sonnensystem.name)+"     <----")
            sternsystemmenu.insert("end",str(alphacentauri.name))
        if sternsystem==alphacentauri:
            sternsystemmenu.insert("end",str(sonnensystem.name))
            sternsystemmenu.insert("end",str(alphacentauri.name)+"     <----")
        
        warpen=tkinter.Button(warptorfenster,text="Warpen",command=warpen)
        warpen.grid(row=2,column=1, pady=5)

        erklarung=tkinter.Button(warptorfenster,text="?",command=warperklarung)
        erklarung.grid(row=3,column=1)

        warptorfenster.protocol("WM_DELETE_WINDOW", game.attributes('-alpha', 1.0))

        #game.attributes('-alpha', 1.0)
    else:
        pass

def weiterfliegen():
    nichtanzeigen=False # variable um keine fluginfos anzuzeigen, wenn man wg. treibstoff nicht reisen kann
    erstereise=False
    global ListeOrte
    global aPlaneten
    global sPlaneten
    global KostenMin
    global KostenMax
    global Geld
    global Ort
    global Laderaum

    

    alterplanet=Ort
    # falls man vom warptor wegfliegt, werden die GUI-Elemente wieder eingeblendet und das warp-fenster geschlossen
    if alterplanet.name=="Warptor":
        warptorfenster.destroy
        for object in warptorhide:
            object.grid()
    # planetenvariable verändern (= fliegen)
    try:
        Nummer = int(ListeOrte.curselection()[0])
    except IndexError: # FALLS NICHTS AUSGEWÄHLT IST (BEI FLUGZIEL)
        pass
    try:
        if sternsystem==sonnensystem:
            Ort = sPlaneten[Nummer+1]
        elif sternsystem==alphacentauri:
            Ort=aPlaneten[Nummer+1]
    except UnboundLocalError:  # FALLS NICHTS AUSGEWÄHLT IST (BEI FLUGZIEL)
        try:
            Ort=Ort
        except NameError: # FALLS NOCH NIE GEFLOGEN WURDE (D.H. MAN IST AUF DEM STARTPLANETEN)
            if sternsystem==sonnensystem:
                Ort=erde
            elif sternsystem==alphacentauri:
                Ort=alphacentauriab
    ortname=Ort.name
    # falls man zu einem warptor geflogen ist, werden die GUI-Elemente versteckt
    if ortname=="Warptor":
        for object in warptorhide:
            object.grid_remove() 
    # TREIBSTOFFVERBRAUCH
    global treibstoff
    treibstoffalt=treibstoff
    entfernungalt=alterplanet.koord
    entfernungneu=Ort.koord
    if entfernungalt>entfernungneu:
        entfernung=entfernungalt-entfernungneu
    else:
        entfernung=entfernungneu-entfernungalt
    abzug=round(((entfernung/1500)*100))
    treibstoff=treibstoff-(treibstoff*(abzug/100))
    if treibstoff<0:
        nichtanzeigen=True
        tkinter.messagebox.showinfo("- A L A R M -","Du kannst nicht nach " + ortname + " reisen.\nDu hast zu wenig Sprit im Tank/einen zu kleinen Tank.\n")
        treibstoff=treibstoffalt
        Ort=alterplanet
    # reiselogs
    with open("logs.txt", "a+") as logs:
        global reisen
        zeit=datetime.now()
        ts=zeit.strftime("%d.%m;%H:%M")
        writetext="REISE\n"+" TS: "+ts+" Reise "+str(reisen+1)+" planet alt: "+str(alterplanet.name)+" planet neu: "+str(Ort.name)+ " entfernung alt: "+str(entfernungalt)+" entfernung neu "+str(entfernungneu)+" entfernung ges: "+str(entfernung)+" abzug: "+str(abzug)+"\n---------------"
        logs.write(writetext)
        logs.write("\n")

    # neues bild in GUI
    global locationImg
    locationImg=Ort.foto

    # Um zu wissen, ob der ort mit "zur" oder "zum" angeredet wird
    global zum
    zum=False

    global zur
    zur=False

    global zu
    zu=False

    if ortname=="Warptor" or ortname=="Mars" or ortname=="Pluto":
        zum=True
    else:
        zur=True
    if sternsystem==alphacentauri:
        zu=True
        zur=False
        zum=False
    # CHANCEN AUF UNVORHERGESEHENES:
    travelnormal=True
    piraten=False
    alien=False
    wurmloch=False
    chance=randint(1,100)
    if chance>10 and chance<=20: # elif damit immer nur eine sache passiert und das and damit ich nur eine variable für die chancen verwenden kann
        travelnormal=False
        piraten=True
    elif chance>20 and chance<=30:
        travelnormal=False
        alien=True
    elif chance>30 and chance<=40:
        travelnormal=False
        wurmloch=True

#-----------------------
    global benutzbareobjekte
    benutzbareobjekte=[]
    for i in range(0,len(objekte)):
        if objekte[i].verkauflich==True:
            benutzbareobjekte.append(objekte[i])
    # Alles normal, puh
    if travelnormal==True:
        if zur==True and nichtanzeigen==False:
            tkinter.messagebox.showinfo("- R E I S E I N F O -","Deine Reise geht zur " + ortname + ".\n Sie verläuft ereignislos.\n")
        if zum==True and nichtanzeigen==False:
            tkinter.messagebox.showinfo("- R E I S E I N F O -","Deine Reise geht zum " + ortname + ".\n Sie verläuft ereignislos.\n")
        if zu==True and nichtanzeigen==False:
            tkinter.messagebox.showinfo("- R E I S E I N F O -","Deine Reise geht zu " + ortname + ".\n Sie verläuft ereignislos.\n")

    # PIRATEN!!!
    elif piraten==True and nichtanzeigen==False:
        if zur==True:
            tkinter.messagebox.showinfo("- A L A R M  -","Auf dem Weg zur " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        if zum==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zum " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        if zu==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zu " + ortname + " wirst du von Piraten überfallen!\nSie stehlen etwas von deinen Materialien und die Hälfte deines Geldes.")
        for i in range(0,len(benutzbareobjekte)):
            chance=randint(1,100)
            if chance>50: # DAMIT NUR BEI CA. DER HÄLFTE DER MATERIALIEN ETWAS GESTOHLEN WIRD
                benutzbareobjekte[i].geladen=benutzbareobjekte[i].geladen//2
        Geld=Geld//2

    # ALIENANGRIFF!!! Ne spaß, sie bemerken dich nicht mal. Also wirklich!
    elif alien==True and sternsystem==alphacentauri and nichtanzeigen==False:
        if zur==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zur " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\n Wer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
        if zum==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zum " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\n Wer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
        if zu==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zu " + ortname + " begegnet dir ein vollkommen unbekanntes Raumschiff!\n Wer sind sie? Was wollen sie? All diese Fragen..\nDoch leider fliegen sie einfach vorbei.. Vielleicht triffst du sie ja nochmal.")
    
    # Alien+Sonnensystem=Asteroid
    elif alien==True and sternsystem==sonnensystem and nichtanzeigen==False:
        if zur==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zur " + ortname + " spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
        if zum==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zum " + ortname + " spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
        if zu==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zu " + ortname + "  spüren deine Sensoren einen Asteroiden auf! Du baust ihn ab und erhältst einige Materialien.")
        for i in range(0,len(benutzbareobjekte)):
            chance=randint(1,100)
            if chance<75: # Damit man bei vielen, aber nicht allen Materialien etwas bekommt
                menge=randint(1,5)
                menge=menge*(randint(1,2)+randint(0,4) )# "zufällige" anzahl an materialien 
                if i>=5:
                    pass
                else:
                    benutzbareobjekte[i].geladen=benutzbareobjekte[i].geladen+menge
                    Laderaum=Laderaum-menge

    # WURMLOCH!!!!
    elif wurmloch==True and nichtanzeigen==False:
        if zur==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zur " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\n Du verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        if zum==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zum " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\n Du verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        if zu==True:
            tkinter.messagebox.showinfo("- A L A R M -","Auf dem Weg zu " + ortname + " erscheint plötzlich ein Wurmloch auf den Sensoren!\n Du verbrauchst viel Treibstoff, kannst aber das Raumschiff retten.\n")
        treibstoff=treibstoff*0.5

    # NEUE KOSTEN FÜR ALLE OBJEKTE
    for i in range (5):
        #KostenDifferenz = KostenMax[i]-KostenMin[i]
        for i in range(0, len(objekte)):
            objekte[i].preis=randint(objekte[i].preismin,objekte[i].preismax)
    reisen=reisen+1
    DisplayAktualisieren()
    Treibstoffaktualisieren()
    warptorcheck()

def plus():
    global EingabeMenge
    alt=int(EingabeMenge.get())
    EingabeMenge.delete("0","end")
    neu=alt+1
    EingabeMenge.insert("end",str(neu))

def minus():
    global EingabeMenge
    alt=int(EingabeMenge.get())
    EingabeMenge.delete("0","end")
    neu=alt-1
    if neu<0:
        neu=0
    EingabeMenge.insert("end",str(neu))

def hilfe():
    Hilfe=tkinter.Toplevel()
    Hilfe.title("Tutorial")
    hilfetext="""Willkommen zu Space Wars!
    Space Wars ist ein interstellarer Handelssimulator. Dein Ziel ist es, durch geschicktes Kaufen und Verkaufen so viel Gewinn wie möglich zu machen!
    \nHier ein kurzes Tutorial:\nIn der Liste oben links findest du die Materialien, die an deinem jetzigen Standort angeboten werden.
    Du kannst sie durch Anklicken auswählen und durch Klicken auf den gleichnamigen Button kaufen.\n\nIn der Liste oben rechts findest du dein Inventar.
    Du kannst auch hier durch Anklicken auswählen und mit dem Button 'Verkaufen' verkaufen.
    \nUnten links findest du eine weitere Liste mit deinen Möglichkeiten zum weiterfliegen.
    Du kannst durch Klicken auswählen und mit dem Button 'Weiterfliegen' genau dies tun.\nMit dem Button 'Neues Spiel' startest du neu,
    und mit dem Button 'Score hochladen' kannst du deinen Score (dein gesammeltes Geld) mit den 10 besten Spielern vergleichen und hochladen.
    \nDanke fürs Spielen und viel Spaß!" 
    """
    erklaerung=tkinter.Label(Hilfe,text=hilfetext)
    erklaerung.grid(row=1,column=1)
    #ListeObjekte.grid_remove()

def online():
    global Geld
    score=Geld
    online=tkinter.Toplevel()
    online.title("Score Vergleichen")

    def hochladen():
        try:
            usernameentry=username.get()
            if len(usernameentry)==0 or usernameentry==" ":
                tkinter.messagebox.showinfo("- F E H L E R -","Bitte gib einen Benutzernamen ein, bevor du etwas hochlädst.")
            else:
                global playerscore
                playerscore=[score,usernameentry]
        except UnboundLocalError:
            tkinter.messagebox.showinfo("- F E H L E R -","Bitte gib einen Benutzernamen ein, bevor du etwas hochlädst.")
        kategorien=[]
        daten=[]
        try:
            # ein versuch, schon existierende daten zu lesen
            with open("score.csv","r") as p:
                read=csv.reader(p)
                kategorien=next(read)
                for row in read:
                    daten.append(row)
        # falls das nicht gelingt:
        except FileNotFoundError:
            pass
        kategorien=["Benutzername","Score"]
        daten.append({playerscore[1],playerscore[0]}) # falls liste schon existiert (s.o.) wird nur angefügt
        # daten schreiben
        with open("score.csv","w") as p:
            writer=csv.writer(p)
            writer.writerow(kategorien)
            writer.writerows(daten)
        # scoreboard aktualisieren
        scoreaktualisieren()
        
    scoretext="Erzielte Punkte: "+str(score)
    scorefeld=tkinter.Label(online,text=scoretext)
    scorefeld.grid(row=1,column=3,pady=5)
    
    username=tkinter.Entry(online)
    username.grid(row=3,column=3)
    usernamelabel=tkinter.Label(online, text="Benutzername:")
    usernamelabel.grid(row=3,column=2)

    upload=tkinter.Button(online,text="Score hochladen",command=hochladen)
    upload.grid(row=4,column=3,pady=5)

    spacer2=tkinter.Label(online,text="|")
    spacer2.grid(row=1,column=1)
    spacer3=tkinter.Label(online,text="|")
    spacer3.grid(row=2,column=1)
    spacer4=tkinter.Label(online,text="|")
    spacer4.grid(row=3,column=1)
    spacer5=tkinter.Label(online,text="|")
    spacer5.grid(row=4,column=1)
    # standardtext auf Label solange nichts geladen ist
    highscorestext="Noch keine Scores vorhanden"
    # label für scoreboard
    highscoreslabel=tkinter.Label(online,text=highscorestext)
    highscoreslabel.grid(row=1,column=0)
    def scoreaktualisieren():
        # listeninitialisierung um daten aus csv zu laden
        daten=[]
        kategorien=[]
        try:
            # daten aus datei laden
            with open("score.csv","r") as p:
                read=csv.reader(p)
                kategorien=next(read)
                for row in read:
                    daten.append(row)
            
            # Daten aus csv in eine liste schreiben
            ganzeliste=[]
            i=0
            for i in range(0,len(daten)):
                ganzeliste.append({kategorien[1]:daten[i][0],kategorien[0]:daten[i][1]})
            
            # in csv ist score als str gespeichert, also zu int machen
            for  i in range(len(ganzeliste)):
                ganzeliste[i]['Score'] = int(ganzeliste[i]['Score'])

            # anhand des scores sortieren (muss aus irgendeinem grund reverse passieren?)
            sortiert = sorted(ganzeliste, key=lambda item: item.get("Score"),reverse=True)

            # wenn mehr als 10 spieler ihre scores hochgeladen haben wird sie automatisch auf die 10 besten gekürzt
            sortiert=sortiert[:10]

            # die liste in eine str packen, um sie auf der GUI im label anzeigen zu können
            highscorestext=""
            for  i in range(0,len(sortiert)):
                highscorestext=highscorestext+"\n"+str(sortiert[i]["Benutzername"])+" : "+str(sortiert[i]["Score"])
            highscoreslabel.config(text=highscorestext)

        # falls csv nicht gefunden wurde
        except FileNotFoundError:
            pass
    scoreaktualisieren()
    


#GUI ----------------------------------------
global ListeObjekte
ListeObjekte = tkinter.Listbox (width=30, height = 10)
ListeObjekte.grid(padx = 5, pady = 5, row = 1, column = 1, columnspan = 1, rowspan=4)

LabelMenge = tkinter.Label(game, text = 'Menge: ')
LabelMenge.grid (row = 1, column = 2)

buttonplus=tkinter.Button(game,text="+",command=plus)
buttonplus.grid(row=1,column=3)

buttonminus=tkinter.Button(game,text="-",command=minus)
buttonminus.grid(row=1,column=5)

EingabeMenge = tkinter.Entry(game, width = 4)
EingabeMenge.grid(row = 1, column = 4)

cb=tkinter.IntVar()
ButtonAlles = tkinter.Checkbutton(game,text="Alles",variable=cb)
ButtonAlles.grid(row=3,column=2,padx=5)

halb=tkinter.IntVar()
ButtonHalfte=tkinter.Checkbutton(game,text="Die Hälfte",variable=halb)
ButtonHalfte.grid(row=3,column=3,padx=5)

ButtonKaufen = tkinter.Button(game, text=' Kaufen  >>> ', command = kaufen)
ButtonKaufen.grid(padx=5, row =2, column = 2, columnspan=2)

ButtonVerkaufen = tkinter.Button(game, text=' <<< Verkaufen ', command = verkaufen)
ButtonVerkaufen.grid(padx=5, row =4, column = 2, columnspan=2)

ListeLaderaum = tkinter.Listbox (width=30, height = 10)
ListeLaderaum.grid(padx = 5, pady = 5, row = 1, column = 6, columnspan = 2, rowspan=4)
#-----------------------
ListeOrte = tkinter.Listbox (width=30, height = 6)
ListeOrte.grid(padx = 5, pady = 20, row = 5, column = 1, columnspan = 1, rowspan=4)

ButtonBewegen = tkinter.Button(game, text = ' Weiterfliegen.. ', command = weiterfliegen)
ButtonBewegen.grid(row=7, column=2, padx=5, columnspan = 2)

ButtonNeustart = tkinter.Button(game, text = ' Neues Spiel ', command = NeuesSpiel)
ButtonNeustart.grid(row=6, column=6, padx=5, pady=25)

hilfebutton=tkinter.Button(game,text="Tutorial",command=hilfe)
hilfebutton.grid(row=8,column=6,pady=5,padx=5)

buttononline=tkinter.Button(game,text="Score hochladen",command=online)
buttononline.grid(row=7,column=6,padx=5,pady=5)
#-----------------------
global TreibstoffZustand
TreibstoffZustand=tkinter.Label(game,text=treibstofftext)
TreibstoffZustand.grid(row=8,column=2,padx=5, columnspan=2)
# ---------------------
global locationImg
locationImg=tkinter.PhotoImage(file="./assets/fotos/ship.gif")
global fotolabel
fotolabel=tkinter.Label(image=locationImg)
fotolabel.grid(row=1,column=0,rowspan=8)
# ---------------------
#liste an widgets die versteckt werden sollen falls man zum warptor gelangt
global warptorhide
warptorhide=[ListeLaderaum,ListeObjekte,ButtonAlles,ButtonHalfte,ButtonKaufen,ButtonVerkaufen,LabelMenge,buttonplus,buttonminus,EingabeMenge]
# ---------------------
def closinglog():
    global Geld
    global reisen
    with open("logs.txt", "a+") as logs:
        global reisen
        zeit=datetime.now()
        ts=zeit.strftime("%d.%m;%H:%M")
        writetext="BEENDEN\n"+"TS: "+ts+"\n"+"Geld: "+str(Geld)+", Reisen: "+str(reisen)+"\n---------------"
        logs.write(writetext)
        logs.write("\n")

def on_closing():
    closinglog()
    game.destroy()

NeuesSpiel()
# ---------------------
try:
    game.protocol("WM_DELETE_WINDOW", on_closing)
    game.mainloop()
except KeyboardInterrupt:
    closinglog()
    game.destroy
