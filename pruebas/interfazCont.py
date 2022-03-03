from ast import Param
from tkinter.messagebox import NO
from pyModbusTCP.client import ModbusClient
# librerias para interfaz
from cgitb import text
from ctypes import alignment
import tkinter as tk
from tkinter.tix import COLUMN
from turtle import left 

# SERVER_HOST = "192.168.25.252"
SERVER_HOST = "192.168.1.43"
SERVER_PORT = 502
dato = list(range(2))
dato.append([1,1,1,1,1,1]) 
client = ModbusClient()

client.host(SERVER_HOST)

client.port(SERVER_PORT)
502
def envio_datos():
    if not client.is_open():
        if not client.open():
            print("no hay conexion "+ SERVER_HOST+":"+str(SERVER_PORT))
    if client.is_open():
        #escritura de parametros
        setpoint = list(range(1))
        # setpoint[0]=2
        # setpoint.append(3)
        # setpoint.append(4)
        # setpoint.append(5)

        setpoint[0]=int(Entrada.get())#deben ser enteros sino la funcion .write_multiple_regsiters() no toma la list
        setpoint.append(int(P.get()))
        setpoint.append(int(I.get()))
        setpoint.append(int(D.get()))
        print(type(setpoint))
        print(setpoint)
        client.write_multiple_registers(9,setpoint)
        print("termino escritura")

def recepcion():
    if not client.is_open():
        if not client.open():
            print("no hay conexion "+ SERVER_HOST+":"+str(SERVER_PORT))
    if client.is_open():
        #falta agregar revisar si los datos llegan bien en el arduino
        # lectura de datos
        print("inicia lectura")
        funcionando = list(range(1))
        funcionando[0] = 0 #la placa lo pone en 1 justo antes de empezar a generar la señal
        while funcionando[0] == 0:
            if  client.read_holding_registers(0,1) == None:
                funcionando[0] = 0
                print("dentro del if none: ")
            else: 
                funcionando = client.read_holding_registers(0,1)
                print("leyendo registro: ",funcionando)
        print("funcionando afuera",funcionando[0])
        #client.write_single_register(6,1)#para que empiece el procesamiento
        while funcionando[0] == 1: #si o si dentro del while tiene que ser una sola lectura por vuelta si no se se pierden datos
        #while dato[-1][0] == 1:
            # print ("entro while 1 \n")
            dato.append(client.read_holding_registers(0,6))#cada lectura comprende salida, e, up, ui, y ud
            funcionando[0]=dato[-1].pop(0) #del ultimo arreglo leido de 6 valores extraigo el primero que corresponde a la 
            # print(funcionando,"\n")         #bandera "funcionando" para preguntar si sigue en 1 y en dato solo dejo los 5 valores de interes
            # time.sleep(0.002)
        del dato[0] #los primeros dos valores del arreglo los toma diferentes (aún no se porque) por eso los elimino
        del dato[0]
        for i in range(len(dato)): #recorro la lista bidimensional para quitar los offset de suma y multiplicacion
            for j in range(len(dato[i])):   #y asi obtener los valores con coma
                dato[i][j] = dato[i][j]/1000-5
        print ("tamaño arreglo", len(dato))
        
        # # Guarda todas las señales juntas en un solo archivo
        # textfile = open("nube.txt", "w")
        # for element in dato:
        #     textfile.write(str(element) + "\n")
        # Solo guarda una señal de las 5 leidas

        # Guarda todas las señales en archivos separados
        #señal 1
        textfile = open("s1.txt", "w")
        for i in range(len(dato)):
            textfile.write(str(dato[i][0]))
            textfile.write("\n")
        textfile.close()
        #señal 2
        textfile = open("s2.txt", "w")
        for i in range(len(dato)):
            textfile.write(str(dato[i][1]))
            textfile.write("\n")
        textfile.close()
        #señal 3
        textfile = open("s3.txt", "w")
        for i in range(len(dato)):
            textfile.write(str(dato[i][2]))
            textfile.write("\n")
        textfile.close()
        #señal 4
        textfile = open("s4.txt", "w")
        for i in range(len(dato)):
            textfile.write(str(dato[i][3]))
            textfile.write("\n")
        textfile.close()
        #señal 5
        textfile = open("s5.txt", "w")
        for i in range(len(dato)):
            textfile.write(str(dato[i][4]))
            textfile.write("\n")
        textfile.close()
        exit() #solo para pruebas

        


        

window = tk.Tk()#define el objeto 
window.title("Planta Motor DC")
window.minsize(600,400)

label = tk.Label(window, text = "Ingresa Parametros del Controlador")
label.grid(column = 0, row = 0)#ubica el label dentro del objeto window

#Definicion de los parametros a ingresar
#proporcional
P = tk.StringVar()
PEntered = tk.Entry(window, width = 15, textvariable = P)#identifica que textbox corresponde al objeto name
PEntered.grid(column = 1, row = 1)#ubica el textbox dentro de la ventana
PEntered.place_info()
labelP = tk.Label(window, text = "Proporcional:")
labelP.grid(column = 0, row =1)
#integral
I =  tk.StringVar()
IEntered = tk.Entry(window, width = 15, textvariable = I)
IEntered.grid(column = 1, row = 2)
labelI = tk.Label(window, text = "Integral:")
labelI.grid(column = 0, row =2)
#derivativo
D =  tk.StringVar()
DEntered = tk.Entry(window, width = 15, textvariable = D)
DEntered.grid(column = 1, row = 3)
labelI = tk.Label(window, text = "Derivativo:")
labelI.grid(column = 0, row =3)
#entrada de referencia
Entrada =  tk.StringVar()
EntradaEntered = tk.Entry(window, width = 15, textvariable = Entrada)
EntradaEntered.grid(column = 1, row = 4)
labelEnt = tk.Label(window, text = "Entrada:", anchor="w")
labelEnt.grid(column = 0, row =4)
# boton envio
button = tk.Button(window, text = "Enviar", command = envio_datos)
button.grid(column= 0, row = 5)

#boton lectura resultados
button2 = tk.Button(window, text = "graficar", command = recepcion)
button2.grid(column= 0, row = 6)

window.mainloop()