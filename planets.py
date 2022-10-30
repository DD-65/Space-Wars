import tkinter
#fenster = tkinter.Tk()
class Planet:
    def __init__(self,name,sonnensystem,koord,warptor,bereisbar,foto):
        self.name=name
        self.sonnensystem=sonnensystem
        self.koord=koord
        self.warptor=warptor
        self.bereisbar=bereisbar
        self.foto=foto

# HIER PLANETEN HINZUFÜGEN // CONTRIBUTE HERE
# Muster: planeten nach sternensystem gruppiert hinzufügen, variablen in der reihenfolge:
# (1) Name: der name des planeten; (2) sonnensystem: das sternsystem, in welchem der planet heimisch ist
# (3) koord: die koordinaten des planeten (d.h. abstand vom zentralstern des sternsystem) (hinweis: pro 5 einheiten wird bei einer reise eine einheit treibstoff abgezogen)
# (4) warptor: boolean, ob der planet ein warptor ist; (5) bereisbar: boolean, ob der planet bereisbar ist (z.B. False für zentralsterne)
# (5) foto: tkinter.photoimage-datei mit pfad zum beschreibenden bild des planeten, GIF-FORMAT, fotos auch in die spieldateien hinzufügen
# neuen planeten dann in die liste des jeweiligen sternsystems schreiben bzw neue erstellen
# vielen dank für die mitarbeit :D

# PLANETENDEFINITION
# PLANETEN DES SONNENSYSTEMS
planeten=[]
sonne=Planet("Sonne","Milchstraße",0,False,False,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
erde=Planet("Erde","Milchstraße",250,False,True,tkinter.PhotoImage(file="./assets/fotos/erde.gif"))
mars=Planet("Mars","Milchstraße",370,False,True,tkinter.PhotoImage(file="./assets/fotos/mars.gif"))
venus=Planet("Venus-Raumstation","Milchstraße",100,False,True,tkinter.PhotoImage(file="./assets/fotos/venus.gif"))
uranus=Planet("Uranus-Raumstation","Milchstraße",600,False,True,tkinter.PhotoImage(file="./assets/fotos/uranus.gif"))
pluto=Planet("Pluto","Milchstraße",1100,False,True,tkinter.PhotoImage(file="./assets/fotos/pluto.gif"))
warptorS=Planet("Warptor","Milchstraße",1000,True,True,tkinter.PhotoImage(file="./assets/fotos/warp.gif"))
# Planeten VON ALPHA CENTAURI
alphacentauria=Planet("Alpha Centauri A (Stern)","Alpha Centauri",0,False,False,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
alphacentauriab=Planet("Alpha Centauri Ab","Alpha Centauri",150,False,True,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
alphacentauribb=Planet("Alpha Centauri Bb","Alpha Centauri",2580,False,True,tkinter.PhotoImage(file="./assets/fotos/ship.gif"))
warptorA=Planet("Warptor","Alpha Centauri",1000,True,True,tkinter.PhotoImage(file="./assets/fotos/warp.gif"))

splaneten= [sonne,erde,mars,venus,uranus,pluto,warptorS] # PlanetEN DES SONNENSYSTEMS
aplaneten=[alphacentauria,alphacentauriab,alphacentauribb,warptorA] # PlanetEN UM ALPHA CENTAURI
planeten=planeten+aplaneten+splaneten

sternsysteme=[]
class Planetensystem:
    def __init__(self, name, planeten, startplanet):
        self.name=name
        self.planeten=planeten
        self.startplanet=startplanet

# HIER STERNENSYSTEME HINZUFÜGEN // CONTRIBUTE HERE
# Muster: sternensysteme hinzufügen, variablen in der reihenfolge:
# (1) name: der name des sternsystems; (2) planeten: liste mit allen planeten des systems (planeten als objekte in die liste)
# (3) startplanet: der planet, auf dem der spieler startet, falls er in diesem system startet
# sternsystem dann in die liste schreiben
# vielen dank für die mitarbeit :D

sonnensystem=Planetensystem("Sonnensystem",splaneten, erde)
alphacentauri=Planetensystem("Alpha Centauri",aplaneten, alphacentauria)
sternsysteme=sternsysteme+[sonnensystem,alphacentauri]