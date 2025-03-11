import tkinter as tk
from controller import (
    plus, minus, kaufen, verkaufen, weiterfliegen, NeuesSpiel,
    hilfe, online, closinglog, sPlaneten, aPlaneten
)
import controller

def setup_gui(game_window):
    # Assign the main window to the controller global
    controller.game = game_window

    # Load images for all planets now that the Tk root exists
    for planet in sPlaneten:
        planet.load_image(game_window)
    for planet in aPlaneten:
        planet.load_image(game_window)

    # Left side: image (current location)
    controller.locationImg = tk.PhotoImage(master=game_window, file="./assets/fotos/ship.gif")
    controller.fotolabel = tk.Label(game_window, image=controller.locationImg)
    controller.fotolabel.grid(row=1, column=0, rowspan=8)

    # Listbox for available objects
    controller.ListeObjekte = tk.Listbox(game_window, width=30, height=10)
    controller.ListeObjekte.grid(padx=5, pady=5, row=1, column=1, columnspan=1, rowspan=4)

    # Menge label, plus/minus buttons, and entry
    LabelMenge = tk.Label(game_window, text='Menge: ')
    LabelMenge.grid(row=1, column=2)
    plus_btn = tk.Button(game_window, text="+", command=plus)
    plus_btn.grid(row=1, column=3)
    minus_btn = tk.Button(game_window, text="-", command=minus)
    minus_btn.grid(row=1, column=5)
    controller.EingabeMenge = tk.Entry(game_window, width=4)
    controller.EingabeMenge.grid(row=1, column=4)

    # Checkbuttons for "Alles" and "Die Hälfte"
    controller.cb = tk.IntVar()
    ButtonAlles = tk.Checkbutton(game_window, text="Alles", variable=controller.cb)
    ButtonAlles.grid(row=3, column=2, padx=5)
    controller.halb = tk.IntVar()
    ButtonHalfte = tk.Checkbutton(game_window, text="Die Hälfte", variable=controller.halb)
    ButtonHalfte.grid(row=3, column=3, padx=5)

    # Kaufen and Verkaufen buttons
    ButtonKaufen = tk.Button(game_window, text=' Kaufen  >>> ', command=kaufen)
    ButtonKaufen.grid(padx=5, row=2, column=2, columnspan=2)
    ButtonVerkaufen = tk.Button(game_window, text=' <<< Verkaufen ', command=verkaufen)
    ButtonVerkaufen.grid(padx=5, row=4, column=2, columnspan=2)

    # Listbox for inventory
    controller.ListeLaderaum = tk.Listbox(game_window, width=30, height=10)
    controller.ListeLaderaum.grid(padx=5, pady=5, row=1, column=6, columnspan=2, rowspan=4)

    # Listbox for travel destinations
    controller.ListeOrte = tk.Listbox(game_window, width=30, height=6)
    controller.ListeOrte.grid(padx=5, pady=20, row=5, column=1, columnspan=1, rowspan=4)

    # Button for traveling
    ButtonBewegen = tk.Button(game_window, text=' Weiterfliegen.. ', command=weiterfliegen)
    ButtonBewegen.grid(row=7, column=2, padx=5, columnspan=2)

    # Neues Spiel button
    ButtonNeustart = tk.Button(game_window, text=' Neues Spiel ', command=NeuesSpiel)
    ButtonNeustart.grid(row=6, column=6, padx=5, pady=25)

    # Tutorial button
    hilfebutton = tk.Button(game_window, text="Tutorial", command=hilfe)
    hilfebutton.grid(row=8, column=6, pady=5, padx=5)

    # Score upload button
    buttononline = tk.Button(game_window, text="Score hochladen", command=online)
    buttononline.grid(row=7, column=6, padx=5, pady=5)

    # Treibstoff label
    controller.TreibstoffZustand = tk.Label(game_window, text="Treibstoff:\n[##########]")
    controller.TreibstoffZustand.grid(row=8, column=2, padx=5, columnspan=2)

    # Set the list of widgets to hide when at a warp gate
    controller.warptorhide = [
        controller.ListeLaderaum, controller.ListeObjekte, ButtonAlles,
        ButtonHalfte, ButtonKaufen, ButtonVerkaufen, LabelMenge,
        plus_btn, minus_btn, controller.EingabeMenge
    ]

    # Start a new game
    NeuesSpiel()

    # Set up window closing protocol
    def on_closing():
        closinglog()
        game_window.destroy()
    game_window.protocol("WM_DELETE_WINDOW", on_closing)