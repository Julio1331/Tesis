from pyModbusTCP.client import ModbusClient
from tkinter import *
import time

SERVER_HOST = "192.168.25.252"
SERVER_PORT = 502
dato = list(range(2))
client = ModbusClient()

client.host(SERVER_HOST)

client.port(SERVER_PORT)
502
def askQuit():
    root.destroy()
    client.close()
# dato[0]=15.24
# dato.append(28.777)
# print (dato[0],dato[1],dato[2])  
# print ("paso while 0 \n")  
def angle(int):
    if not client.is_open():
        if not client.open():
            print("no hay conexion "+ SERVER_HOST+":"+str(SERVER_PORT))

    if client.is_open():
        client.write_single_register(13,slider.get())

   # if client.is_open():
        leer =list(range(1))
        leer[0] = 1
        funcionando = list(range(1))
        funcionando[0] = 0
        while funcionando[0] == 0:
            funcionando = client.read_holding_registers(0,1)#para saber cuando empezar a leer datos
            print("dentro while 0: ",funcionando)
            print (dato[1])
        print("funcionando afuera",funcionando[0])
        client.write_single_register(6,1)#para que empiece el procesamiento
        while (funcionando[0] == 1):
            print ("entro while 1 \n")
            dato.append(client.read_holding_registers(2,1))#cada lectura comprende salida, e, up, ui, y ud
            funcionando = client.read_holding_registers(0,1)
            print(funcionando [0], dato[-1])
            time.sleep(0.002)
        print ("tamaño arreglo", len(dato))
        
        
        textfile = open("nube.txt", "w")
        for element in dato:
            textfile.write(str(element) + "\n")
        textfile.close()
        # for i in range(0,30):
        #     dato[i]=dato[i]/1000-5
        
    time.sleep(0.1)


root = Tk()
root.protocol("WM_DELETE_WINDOW", askQuit)
root.title('Python-ESP8266')
slider = Scale(root, from_=0, to=180, orient=HORIZONTAL,command=angle,length=400)
slider.pack()
root.minsize(500,30)
root.mainloop()
