from game import plus, minus, kaufen, verkaufen, weiterfliegen, neuesspiel, hilfe, online
fenster = tkinter.Tk()
import tkinter
# GUI-Objekte
global listeobjekte
listeobjekte = tkinter.Listbox (width=30, height = 10)
listeobjekte.grid(padx = 5, pady = 5, row = 1, column = 1, columnspan = 1, rowspan=4)

labelmenge = tkinter.Label(fenster, text = 'Menge: ')
labelmenge.grid (row = 1, column = 2)

buttonplus=tkinter.Button(fenster,text="+",command=plus)
buttonplus.grid(row=1,column=3)

buttonminus=tkinter.Button(fenster,text="-",command=minus)
buttonminus.grid(row=1,column=5)

eingabemenge = tkinter.Entry(fenster, width = 4)
eingabemenge.grid(row = 1, column = 4)

cb=tkinter.IntVar()
buttonalles = tkinter.Checkbutton(fenster,text="Alles",variable=cb)
buttonalles.grid(row=3,column=2,padx=5)

halb=tkinter.IntVar()
buttonhalfte=tkinter.Checkbutton(fenster,text="Die Hälfte",variable=halb)
buttonhalfte.grid(row=3,column=3,padx=5)

buttonkaufen = tkinter.Button(fenster, text=' Kaufen  >>> ', command = kaufen)
buttonkaufen.grid(padx=5, row =2, column = 2, columnspan=2)

buttonverkaufen = tkinter.Button(fenster, text=' <<< Verkaufen ', command = verkaufen)
buttonverkaufen.grid(padx=5, row =4, column = 2, columnspan=2)

listeladeraum = tkinter.Listbox (width=30, height = 10)
listeladeraum.grid(padx = 5, pady = 5, row = 1, column = 6, columnspan = 2, rowspan=4)
#-----------------------
listeorte = tkinter.Listbox (width=30, height = 6)
listeorte.grid(padx = 5, pady = 20, row = 5, column = 1, columnspan = 1, rowspan=4)

buttonbewegen = tkinter.Button(fenster, text = ' Weiterfliegen.. ', command = weiterfliegen)
buttonbewegen.grid(row=7, column=2, padx=5, columnspan = 2)

buttonneustart = tkinter.Button(fenster, text = ' Neues Spiel ', command = neuesspiel)
buttonneustart.grid(row=6, column=6, padx=5, pady=25)

hilfebutton=tkinter.Button(fenster,text="Tutorial",command=hilfe)
hilfebutton.grid(row=8,column=6,pady=5,padx=5)

buttononline=tkinter.Button(fenster,text="Score hochladen",command=online)
buttononline.grid(row=7,column=6,padx=5,pady=5)
#-----------------------
treibstofftext="Treibstoff:\n[##########]"
global treibstoffzustand
treibstoffzustand=tkinter.Label(fenster,text=treibstofftext)
treibstoffzustand.grid(row=8,column=2,padx=5, columnspan=2)
# ---------------------
global locationImg
locationImg=tkinter.PhotoImage(file="./assets/fotos/ship.gif")
global fotolabel
fotolabel=tkinter.Label(image=locationImg)
fotolabel.grid(row=1,column=0,rowspan=8) 

#liste an widgets die versteckt werden sollen falls man zum warptor gelangt
warptorhide=[listeladeraum, listeobjekte, buttonalles, buttonhalfte, buttonkaufen, buttonverkaufen, labelmenge, buttonplus, buttonminus, eingabemenge]

# loop
fenster.mainloop()