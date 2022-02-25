
from pyModbusTCP.client import ModbusClient
from tkinter import *
import time

SERVER_HOST = "192.168.25.252"
#SERVER_HOST = "192.168.1.33"
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
        funcionando = list(range(1))
        funcionando[0] = 0
        while funcionando[0] == 0:
            funcionando = client.read_holding_registers(0,1)#para saber cuando empezar a leer datos
            print("dentro while 0: ",funcionando)
        print("funcionando afuera",funcionando[0])
        #client.write_single_register(6,1)#para que empiece el procesamiento
        while funcionando[0] == 1:
            print ("entro while 1 \n")
            dato.append(client.read_holding_registers(0,6))#cada lectura comprende salida, e, up, ui, y ud
            funcionando[0]=dato[-1].pop(0)
            #funcionando = client.read_holding_registers(0,1)
            #print(dato)
            print(funcionando,"\n")
            # time.sleep(0.002)
        del dato[0]
        del dato[0]
        print(type(dato))
        print(type(dato[0]))
        print(type(dato[0][0]))
        for i in range(len(dato)):
            for j in range(len(dato[i])):
                dato[i][j] = dato[i][j]/1000-5
        print ("tamaño arreglo", len(dato))
        
        # Guarda todas las señales juntas
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
        exit()
        # for i in range(0,30):
        #     dato[i]=dato[i]/1000-5
        
    #time.sleep(0.1)


root = Tk()
root.protocol("WM_DELETE_WINDOW", askQuit)
root.title('Python-ESP8266')
slider = Scale(root, from_=0, to=180, orient=HORIZONTAL,command=angle,length=400)
slider.pack()
root.minsize(500,30)
root.mainloop()
