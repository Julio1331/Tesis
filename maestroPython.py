from pyModbusTCP.client import ModbusClient
from tkinter import *
import time

SERVER_HOST = "192.168.1.150"
SERVER_PORT = 502

client = ModbusClient()

client.host(SERVER_HOST)
'192.168.1.50'
client.port(SERVER_PORT)
502
def askQuit():
    root.destroy()
    client.close()
    
def angle(int):
    if not client.is_open():
        if not client.open():
            print("no hay conexion "+ SERVER_HOST+":"+str(SERVER_PORT))

    if client.is_open():
        client.write_single_register(0,slider.get())

    time.sleep(0.1)

root = Tk()
root.protocol("WM_DELETE_WINDOW", askQuit)
root.title('Python-ESP8266')
slider = Scale(root, from_=0, to=180, orient=HORIZONTAL,command=angle,length=400)
slider.pack()
root.minsize(500,30)
root.mainloop()
