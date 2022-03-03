
import requests # PARA TRANSMISION A SERVIDOR
from pyModbusTCP.client import ModbusClient
from tkinter import *
import time


SERVER_HOST = "192.168.25.252"
# SERVER_HOST = "192.168.1.43"
SERVER_PORT = 502
dato = list(range(2))
client = ModbusClient()

client.host(SERVER_HOST)

client.port(SERVER_PORT)
502
def askQuit(): #metodo para cerrar la ventana del slicer
    root.destroy()
    client.close()

def angle(int):
    if not client.is_open():
        if not client.open():
            print("no hay conexion "+ SERVER_HOST+":"+str(SERVER_PORT))

    if client.is_open():
        client.write_single_register(13,slider.get())

   # if client.is_open():#si colocaba este if no funcionaba bien
        funcionando = list(range(1))
        funcionando[0] = 0 #la placa lo pone en 1 justo antes de empezar a generar la señal
        while funcionando[0] == 0:
            funcionando = client.read_holding_registers(0,1)#para saber cuando empezar a leer datos
            print("dentro while 0: ",funcionando)
        print("funcionando afuera",funcionando[0])
        #client.write_single_register(6,1)#para que empiece el procesamiento
        while funcionando[0] == 1: #si o si dentro del while tiene que ser una sola lectura por vuelta si no se se pierden datos
            print ("entro while 1 \n")
            dato.append(client.read_holding_registers(0,6))#cada lectura comprende salida, e, up, ui, y ud
            funcionando[0]=dato[-1].pop(0) #del ultimo arreglo leido de 6 valores extraigo el primero que corresponde a la 
            print(funcionando,"\n")         #bandera "funcionando" para preguntar si sigue en 1 y en dato solo dejo los 5 valores de interes
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
        # #señal 1
        # textfile = open("s1.txt", "w")
        # for i in range(len(dato)):
        #     textfile.write(str(dato[i][0]))
        #     textfile.write("\n")
        # textfile.close()
        # #señal 2
        # textfile = open("s2.txt", "w")
        # for i in range(len(dato)):
        #     textfile.write(str(dato[i][1]))
        #     textfile.write("\n")
        # textfile.close()
        # #señal 3
        # textfile = open("s3.txt", "w")
        # for i in range(len(dato)):
        #     textfile.write(str(dato[i][2]))
        #     textfile.write("\n")
        # textfile.close()
        # #señal 4
        # textfile = open("s4.txt", "w")
        # for i in range(len(dato)):
        #     textfile.write(str(dato[i][3]))
        #     textfile.write("\n")
        # textfile.close()
        # #señal 5
        # textfile = open("s5.txt", "w")
        # for i in range(len(dato)):
        #     textfile.write(str(dato[i][4]))
        #     textfile.write("\n")
       #  textfile.close()

    ## PARA TRANSMITIR DATOS A SERVIDOR
    datoT = [[dato[j][i] for j in range(len(dato))] for i in range(len(dato[0]))]
    sample = list(range(1,100))
    pload = {'base': sample, 's1': datoT[0], 's2': datoT[1], 's3': datoT[2], 's4': datoT[3], 's5': datoT[4]}
    r = requests.post('http://rers.dyndns.org:7666/post', data = pload)
    print(r.status_code)
    print(r.text)
    exit()
        
    #time.sleep(0.1)

#ventana slicer
root = Tk()
root.protocol("WM_DELETE_WINDOW", askQuit)
root.title('Python-ESP8266')
slider = Scale(root, from_=0, to=180, orient=HORIZONTAL,command=angle,length=400)
slider.pack()
root.minsize(500,30)
root.mainloop()
