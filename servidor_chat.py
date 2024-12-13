#Librerias Utilizadas
import socket
import threading

#especificamos direccion y puerto
host = '127.0.0.1'
port = 4343

#creacion del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#datos de conexion e inicio del servidor
server.bind((host, port))
server.listen()
print(f" PenguServer iniciado {host}:{port}")

#listas para guardar datos de clientes y sus usuarios
clientes = []
usuarios = []

#envio de mensajes de usuarios a otros usuarios
def broadcast(mensaje, cliente_emisor):
    """
    Envía un mensaje a todos los clientes excepto al emisor.
    Se validan los casos de mensajes vacíos o demasiado largos.
    """
    # Validar que el mensaje no sea vacío
    if not mensaje.strip():
        print("Mensaje vacío, no se enviará.")
        return

    # Validar que el mensaje no exceda un tamaño permitido (ejemplo: 128 bytes)
    if len(mensaje) > 128:
        print("Mensaje demasiado largo, no se enviará.")
        return

    # Enviar el mensaje a todos los clientes excepto al emisor
    for cliente in clientes:
        if cliente != cliente_emisor:  # Excluir al emisor
            try:
                cliente.send(mensaje)
            except ConnectionError as e:
                print(f"Error al enviar el mensaje a {cliente}: {e}")




#Para desconexion del usuarios
def disconnected_client(client):
    index = clientes.index(client)
    usuario = usuarios[index]
    broadcast(f"PenguBot: [{usuario} ha abandonado el chat]".encode('utf-8'),client)
    clientes.remove(client)
    usuarios.remove(usuario)
    client.close()
    print(f"El usuario [{usuario}] se ha desconectado")


#mensaje de los usuarios
def handle_messages(client):
    while True:
        try:
            message = client.recv(128)
            broadcast(message,client)
        except:
            disconnected_client(client)
            break


#aceptacion de conexiones
def receive_connections():
    while True:
        client , address = server.accept()

        client.send("@username".encode("utf-8"))
        usuario = client.recv(128).decode("utf-8")

        clientes.append(client)
        usuarios.append(usuario)

        print(f"[{usuario}] se acaba de conectar al servidor {str(address)}")

        message = f"PenguBot: {usuario} se ha conectado!".encode("utf-8")
        broadcast(message, client)
        client.send("Ya estas conectado al PenguChat!".encode("utf-8"))

        thread = threading.Thread(target=handle_messages , args=(client,))
        thread.start()

def cambiar_nombre(cliente, nuevo_nombre):
    try:
        index = clientes.index(cliente)
        antiguo_nombre = usuarios[index]
        usuarios[index] = nuevo_nombre
        mensaje = f"Tu nombre ha sido cambiado de {antiguo_nombre} a {nuevo_nombre}"
        cliente.send(mensaje.encode('utf-8'))
        broadcast(f"PenguBot: {antiguo_nombre} ahora es conocido como {nuevo_nombre}".encode('utf-8'), cliente)
    except ValueError:
        # El cliente no está en la lista
        print(f"Error: El cliente {cliente} no está registrado.")
    except Exception as e:
        print(f"Error al cambiar el nombre: {e}")


if __name__ == "__main__":
    receive_connections()