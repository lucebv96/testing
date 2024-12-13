#librerias utilizadas
import socket
import threading
import os
import time


#Diseño xd
if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"


time.sleep(1)

os.system(var)

print('*********************************')
print('*                               *')
print('*    BIENVENIDO A PenguCHAT!    *')
print('*                               *')
print('*********************************')

time.sleep(1)
os.system(var)

print('*********************************')
print('*                               *')
print('*   Aqui puedes chatear con     *')
print('*   los Pingüinos conectados    *')
print('*                               *')
print('*********************************')


time.sleep(1)

os.system(var)

print('*********************************')
print('*                               *')
print('*    BIENVENIDO A PenguCHAT!    *')
print('*                               *')
print('*********************************')



usuario = input("\nIngrese su nombre de usuario: ")

#datos de conexion
host = '127.0.0.1'
port = 4343

#creacion del socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive_messages():
    while True:
        try:
            message = client.recv(128).decode('utf-8')

            if message == '@username':
                client.send(usuario.encode('utf-8'))
        
            else:
                print(message)
        except:
            print('Error! Algo salio mal')
            client.close
            break


#envio mensajes
def write_messages():
    while True:
        message = f"{usuario}: {input('')}"
        client.send(message.encode('utf-8'))



# Hilos usuario
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)  
write_thread.start()