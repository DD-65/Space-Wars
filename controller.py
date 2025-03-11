from game_logic import attempt_warp
from utils import find_planet
from strings import MESSAGES

class GameController:
    def __init__(self, player, planets):
        self.player = player
        self.planets = planets

    def warp_to_planet(self, planet_name):
        target_planet = find_planet(self.planets, planet_name)
        if not target_planet:
            return False, MESSAGES["error"]

        success, message = attempt_warp(self.player, target_planet.system)

        if success:
            self.player.current_planet = target_planet

        return success, message