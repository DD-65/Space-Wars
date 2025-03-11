from config import INITIAL_CREDITS, INITIAL_FUEL

class Planet:
    def __init__(self, name, system, coords, warp_gate, bereisbar, foto_path):
        self.name = name
        self.system = system
        self.coords = coords
        self.warp_gate = warp_gate
        self.bereisbar = bereisbar
        self.foto_path = foto_path
        self.foto = None

    def load_image(self, master):
        import tkinter
        self.foto = tkinter.PhotoImage(master=master, file=self.foto_path)

class Item:
    def __init__(self, name, base_price, price_max, price_min, loaded, default_system, sellable, buyable):
        self.name = name
        self.base_price = base_price = base_price
        self.price_max = price_max
        self.price_min = price_min
        self.loaded = loaded
        self.default_system = default_system
        self.sellable = sellable
        self.buyable = buyable

class Ship:
    def __init__(self, cargo_capacity=100, fuel_capacity=1000):
        self.cargo_capacity = cargo_capacity
        self.fuel_capacity = fuel_capacity
        self.fuel = fuel_capacity
        self.cargo = {}

class Market:
    def __init__(self, items):
        self.prices = {item.name: item.base_price for item in items}

    def get_price(self, item_name):
        return self.prices.get(item_name, None)

class Player:
    def __init__(self, name, starting_planet):
        self.name = name
        self.credits = INITIAL_CREDITS
        self.current_planet = starting_planet
        self.current_system = starting_planet.system
        self.ship = Ship()
        self.inventory = {}