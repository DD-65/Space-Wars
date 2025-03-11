from config import WARP_COST
from strings import MESSAGES
from event_manager import EventManager

def attempt_warp(player, target_system):
    if player.credits < WARP_COST:
        return False, MESSAGES["warp_insufficient_funds"]

    player.credits -= WARP_COST
    player.current_system = target_system

    event = EventManager.trigger()
    if event:
        return True, handle_event(event, player, target_system)

    return True, MESSAGES["warp_success"]

def handle_event(event, player, destination):
    if event == "pirate_attack":
        return MESSAGES["travel_pirates"].format(destination=destination)
    elif event == "alien_contact":
        return MESSAGES["alien_encounter"]
    elif event == "wormhole":
        return MESSAGES["wormhole_encounter"]
    return ""