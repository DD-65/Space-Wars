from planets import sonnensystem
class Objekt:
    def __init__(self, name, preis, preismax, preismin, stdsystem = "all", geladen = 0, verkauflich = True, kaufbar = True, upgrade = False):
        self.name = name
        self.preis = preis
        self.preismax = preismax
        self.preismin = preismin
        self.geladen = geladen
        self.stdsystem = stdsystem
        self.verkauflich = verkauflich
        self.kaufbar = kaufbar
        self.upgrade = upgrade

# HIER OBJEKTE HINZUFÜGEN // CONTRIBUTE HERE
# TODO: genauere beschreibung des contribute-prozesses
# vielen dank für die mitarbeit :D
# Objektdefinition
objekte=[]
eisen=Objekt("Eisen",250,1350,100,sonnensystem)
h2o=Objekt("H2O",750,1700,200,sonnensystem)
co2=Objekt("CO2",600,2000,200,sonnensystem)
titan=Objekt("Titan",380,1800,150,sonnensystem)
lithium=Objekt("Lithium",1000,7500,400,sonnensystem)
treibstoffobj=Objekt("Treibstoff (10% Tankfüllung)",3500,3500,3500,verkauflich=False)
tankup=Objekt("Tank-Upgrade",100000,100000,100000,verkauflich=False, upgrade=True)
ladeup=Objekt("Laderaum-Vergrößerung",100000,10000,10000,verkauflich=False, upgrade=True)
testing=Objekt("Testing",0,0,0,kaufbar=False,verkauflich=False)
objekte=objekte+[eisen,h2o,co2,titan,lithium,treibstoffobj,tankup,ladeup,testing]

# liste aller upgrades
allupgrades = []
# liste aller benutzbaren (d.h. verkaufbaren) objekte
benutzbareobjekte = []

# füllen der listen
for i in objekte:
    if i.verkauflich:
        benutzbareobjekte.append(i)
    if i.upgrade:
        allupgrades.append(i)
