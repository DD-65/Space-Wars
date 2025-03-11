import random
from config import ALIEN_ENCOUNTER_CHANCE, PIRATE_ENCOUNTER_CHANCE

class EventManager:
    EVENTS = [
        ("pirate_attack", PIRATE_ENCOUNTER_CHANCE),
        ("alien_contact", ALIEN_ENCOUNTER_CHANCE),
        ("wormhole", 0.02)
    ]

    @staticmethod
    def trigger():
        for event, chance in EventManager.EVENTS:
            if random.random() < chance:
                return event
        return None