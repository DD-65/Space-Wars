import tkinter as tk
from gui import setup_gui

def main():
    game = tk.Tk()
    game.title("Space Wars")
    setup_gui(game)
    game.mainloop()

if __name__ == "__main__":
    main()