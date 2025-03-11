import tkinter

class Planet:
    def __init__(self, name, sonnensystem, koord, warptor, bereisbar, foto_path):
        self.name = name
        self.sonnensystem = sonnensystem
        self.koord = koord
        self.warptor = warptor
        self.bereisbar = bereisbar
        self.foto_path = foto_path
        self.foto = None  # Image will be loaded later when a Tk root exists

    def load_image(self, master):
        self.foto = tkinter.PhotoImage(master=master, file=self.foto_path)

class Planetensystem:
    def __init__(self, name, planeten, startplanet):
        self.name = name
        self.planeten = planeten
        self.startplanet = startplanet

class Objekt:
    def __init__(self, name, preis, preismax, preismin, geladen, stdsystem, verkauflich, kaufbar):
        self.name = name
        self.preis = preis
        self.preismax = preismax
        self.preismin = preismin
        self.geladen = geladen
        self.stdsystem = stdsystem
        self.verkauflich = verkauflich
        self.kaufbar = kaufbar