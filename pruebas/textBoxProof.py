import tkinter as tk 
from tkinter import ttk #ttk da mayor libertad de configuracion pero mas trabajo, a diferencia de tk
#que permite menos personalizacion pero usa configuraciones estandar


window = tk.Tk()#define el objeto 
window.title("Python Tkinter Text Box")
window.minsize(600,400)

def clickMe():#accion a realizar cuando el usuario de click en el boton
    label.configure(text= 'Hello ' + name.get() + ' ' + name1.get())
    print(name.get())

label = ttk.Label(window, text = "Enter Your Name")#define el objeto label y dice que va dentro del objeto
    #window ya definido 
label.grid(column = 0, row = 0)#ubica el label dentro del objeto window



#defiene los objetos, los lugares en la ventana y que lugar corresponde a cada objeto
name = tk.StringVar()#define objeto donde se guardará lo que ingrese el usuario
nameEntered = ttk.Entry(window, width = 15, textvariable = name)#identifica que textbox corresponde al objeto name
nameEntered.grid(column = 1, row = 1)#ubica el textbox dentro de la ventana
name1 =  tk.StringVar()
name1Entered = ttk.Entry(window, width = 15, textvariable = name1)
name1Entered.grid(column = 1, row = 2)


button = ttk.Button(window, text = "Click Me", command = clickMe)#define el objeto boton y lo enlaza
#al comando clickMe

button.grid(column= 0, row = 2)#tamaño del boton

window.mainloop()#este metodo se usa cuando la aplicacion ya esta lista para ejecutarse
#es un bucle infinito mientras el objeto windows no se cierre 