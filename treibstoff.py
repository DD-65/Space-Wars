from settings import MAX_TREIBSTOFF, treibstoff
from objects import treibstoffobj

treibstoffmax = MAX_TREIBSTOFF


def treibstoffaktualiseren(treibstofflabel):
    global treibstoff
    try:
        geladenerT = treibstoffobj.geladen
    except IndexError: # FALLS KEIN TREIBSTOFF GELADEN
        geladenerT = 0
    treibstoff += (geladenerT*10)
    treibstoffobj.geladen=0
    treibstofftext = "Treibstoff:\n"+"["
    treibstoff = int(treibstoff)
    for i in range(1,(treibstoff//10)+1): # PRO 10% DES TREIBSTOFFS EIN STRICH IN DER GUI
        treibstofftext+="#"
    if (treibstoff//10)<(treibstoffmax//10):
        zahler=(treibstoffmax//10)-(treibstoff//10)
        for i in range(0,zahler+1):
            treibstofftext+="-"
    treibstofftext+="]"
    treibstofflabel["text"]=treibstofftext

def treibstoffkaufen(menge,treibstofflabel):
    treibstoffobj.geladen += menge
    treibstoffaktualiseren(treibstofflabel)

def treibstoffverbrauch(treibstofflabel, planet1, planet2):
    global treibstoff
    planetabstand = abs(planet2.koord - planet1.koord)
    abzug = planetabstand // 5
    treibstoff -= abzug
    treibstoffaktualiseren(treibstofflabel)
    return abzug