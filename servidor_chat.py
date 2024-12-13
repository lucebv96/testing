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
    # Buscamos el índice del cliente en la lista
    index = clientes.index(cliente)
    # Cambiamos el nombre en la lista de usuarios
    usuarios[index] = nuevo_nombre
    # Enviamos un mensaje de confirmación al cliente
    cliente.send(f"Tu nombre ha sido cambiado a {nuevo_nombre}".encode('utf-8'))


if __name__ == "__main__":
    receive_connections()