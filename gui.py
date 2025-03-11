import tkinter as tk
from tkinter import messagebox
from models import Player
from utils import load_planets, load_items, find_planet
from game_logic import attempt_warp
from strings import MESSAGES
from config import DEFAULT_START_PLANET

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Wars - Trading Simulator")

        self.planets = load_planets()
        self.items = load_items()

        start_planet = find_planet(self.planets, DEFAULT_START_PLANET)
        self.player = Player("Spieler1", start_planet)

        self.create_widgets()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text=f"Aktueller Standort: {self.player.current_planet.name}")
        self.info_label.pack(pady=10)

        self.credits_label = tk.Label(self.root, text=f"Credits: {self.player.credits}")
        self.credits_label.pack(pady=10)

        self.warp_button = tk.Button(self.root, text="Warp", command=self.warp)
        self.warp_button.pack(pady=10)

    def warp(self):
        available_planets = [
            planet.name for planet in self.planets
            if planet != self.player.current_planet and planet.bereisbar
        ]
        if not available_planets:
            messagebox.showinfo(MESSAGES["error"], "Keine verfügbaren Ziele für Warp.")
            return

        selected_planet = available_planets[0]  # Expandable later with proper UI choice
        target_planet = find_planet(self.planets, selected_planet)

        success, message = attempt_warp(self.player, target_planet.system)

        if success:
            self.player.current_planet = target_planet
            self.info_label.config(text=f"Aktueller Standort: {self.player.current_planet.name}")
            self.credits_label.config(text=f"Credits: {self.player.credits}")

        messagebox.showinfo(MESSAGES["warp_status"], message)