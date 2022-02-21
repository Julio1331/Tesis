from cgitb import text
from ctypes import alignment
import tkinter as tk
from tkinter.tix import COLUMN
from turtle import left 



window = tk.Tk()#define el objeto 
window.title("Planta Motor DC")
window.minsize(600,400)

label = tk.Label(window, text = "Ingresa Parametros del Controlador")
label.grid(column = 0, row = 0)#ubica el label dentro del objeto window

#defiene los objetos, los lugares en la ventana y que lugar corresponde a cada objeto
P = tk.StringVar()#define objeto donde se guardará lo que ingrese el usuario
PEntered = tk.Entry(window, width = 15, textvariable = P)#identifica que textbox corresponde al objeto name
PEntered.grid(column = 1, row = 1)#ubica el textbox dentro de la ventana
PEntered.place_info()
labelP = tk.Label(window, text = "Proporcional:")
labelP.grid(column = 0, row =1)
I =  tk.StringVar()
IEntered = tk.Entry(window, width = 15, textvariable = I)
IEntered.grid(column = 1, row = 2)
labelI = tk.Label(window, text = "Integral:")
labelI.grid(column = 0, row =2)
D =  tk.StringVar()
DEntered = tk.Entry(window, width = 15, textvariable = D)
DEntered.grid(column = 1, row = 3)
labelI = tk.Label(window, text = "Derivativo:")
labelI.grid(column = 0, row =3)
Entrada =  tk.StringVar()
EntradaEntered = tk.Entry(window, width = 15, textvariable = Entrada)
EntradaEntered.grid(column = 1, row = 4)
labelEnt = tk.Label(window, text = "Entrada:", anchor="w")
labelEnt.grid(column = 0, row =4)


def envio_datos():#accion a realizar cuando el usuario de click en el boton
    label.configure(text= 'boton')
button = tk.Button(window, text = "Enviar", command = envio_datos)#define el objeto boton y lo enlaza
#al comando clickMe

button.grid(column= 0, row = 5)#tamaño del boton


window.mainloop()#este metodo se usa cuando la aplicacion ya esta lista para ejecutarse
#es un bucle infinito mientras el objeto windows no se cierre 