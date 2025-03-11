import json
from models import Planet, Item

def load_planets(filepath="planets.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        planets_data = json.load(file)
    return [Planet(**planet) for planet in planets_data]

def load_items(filepath="items.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        items_data = json.load(file)
    return [Item(**item) for item in items_data]

def find_planet(planets, planet_name):
    for planet in planets:
        if planet.name == planet_name:
            return planet
    return None