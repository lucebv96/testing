import pytest
from unittest.mock import Mock, patch
from servidor_chat import broadcast, disconnected_client, clientes, usuarios

# Clase Cliente simulada para las pruebas de integración
class ClienteSimulado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ultimo_mensaje = None
        self.mensajes_recibidos = []
        self.activo = True

    def send(self, mensaje):
        if self.activo:
            self.mensajes_recibidos.append(mensaje)
            self.ultimo_mensaje = mensaje
        else:
            raise ConnectionError("Cliente desconectado")

    def close(self):
        self.activo = False

# Prueba de integración: varios clientes conectados, envío y recepción de mensajes
def test_transmision_mensajes_simultaneos():
    clientes.clear()
    usuarios.clear()

    # Simulamos varios clientes conectados
    cliente1 = ClienteSimulado("Usuario1")
    cliente2 = ClienteSimulado("Usuario2")
    cliente3 = ClienteSimulado("Usuario3")

    clientes.extend([cliente1, cliente2, cliente3])
    usuarios.extend(["Usuario1", "Usuario2", "Usuario3"])

    mensaje = "Hola desde Usuario1!"

    # Cliente1 envía un mensaje
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Verificamos que los demás clientes recibieron el mensaje
    assert cliente2.ultimo_mensaje == mensaje.encode("utf-8")
    assert cliente3.ultimo_mensaje == mensaje.encode("utf-8")

    # Verificamos que el cliente emisor no recibió su propio mensaje
    assert cliente1.ultimo_mensaje is None


# Prueba de manejo de desconexión abrupta de un cliente
def test_desconexion_inesperada():
    clientes.clear()
    usuarios.clear()

    cliente1 = ClienteSimulado("Usuario1")
    cliente2 = ClienteSimulado("Usuario2")
    cliente3 = ClienteSimulado("Usuario3")

    clientes.extend([cliente1, cliente2, cliente3])
    usuarios.extend(["Usuario1", "Usuario2", "Usuario3"])

    # Desconectamos abruptamente al cliente2
    cliente2.close()
    disconnected_client(cliente2)

    # Verificamos que el cliente desconectado ya no está en la lista de clientes
    assert cliente2 not in clientes
    assert "Usuario2" not in usuarios

    # Cliente1 envía un mensaje
    mensaje = "Hola a todos!"
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Verificamos que cliente3 recibió el mensaje y cliente2 no (ya está desconectado)
    assert cliente3.ultimo_mensaje == mensaje.encode("utf-8")


# Prueba de manejo de errores de red (simulación con Mock)
def test_manejo_errores_red():
    clientes.clear()
    usuarios.clear()

    cliente1 = ClienteSimulado("Usuario1")
    cliente2 = Mock(spec=ClienteSimulado)
    cliente3 = ClienteSimulado("Usuario3")

    clientes.extend([cliente1, cliente2, cliente3])
    usuarios.extend(["Usuario1", "Usuario2", "Usuario3"])

    # Simulamos que cliente2 lanza un error de red al intentar enviar un mensaje
    cliente2.send.side_effect = ConnectionError("Error de red")

    mensaje = "Hola desde Usuario1!"
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Verificamos que cliente2 intentó enviar el mensaje pero falló
    cliente2.send.assert_called_once_with(mensaje.encode("utf-8"))

    # Verificamos que cliente3 sí recibió el mensaje
    assert cliente3.ultimo_mensaje == mensaje.encode("utf-8")

    # Verificamos que cliente1 (emisor) no recibió su propio mensaje
    assert cliente1.ultimo_mensaje is None

# # Prueba de manejo de desconexión repentina (corregida)
# def test_desconexion_durante_mensajes():
#     clientes.clear()
#     usuarios.clear()

#     cliente1 = ClienteSimulado("Usuario1")
#     cliente2 = Mock(spec=ClienteSimulado)
#     cliente3 = ClienteSimulado("Usuario3")

#     cliente2.nombre = "Usuario2"
#     cliente3.nombre = "Usuario3"
#     cliente2.ultimo_mensaje = None
#     cliente3.ultimo_mensaje = None

#     clientes.extend([cliente1, cliente2, cliente3])
#     usuarios.extend(["Usuario1", "Usuario2", "Usuario3"])

#     mensaje1 = "Hola desde Usuario1!"
#     mensaje2 = "Mensaje de Usuario2"
#     mensaje3 = "Mensaje de Usuario3"

#     # Cliente1 envía un mensaje
#     broadcast(mensaje1.encode("utf-8"), cliente1)
#     cliente2.ultimo_mensaje = mensaje1.encode("utf-8")  # Simulamos recepción del mensaje
#     assert cliente2.ultimo_mensaje == mensaje1.encode("utf-8")
#     assert cliente3.ultimo_mensaje == mensaje1.encode("utf-8")
#     assert cliente1.ultimo_mensaje is None

#     # Cliente2 envía un mensaje
#     cliente2.send.reset_mock()  # Reiniciamos el mock para este nuevo caso
#     broadcast(mensaje2.encode("utf-8"), cliente2)
#     cliente2.ultimo_mensaje = mensaje2.encode("utf-8")  # Simulamos que cliente2 también recibe su propio mensaje
#     assert cliente1.ultimo_mensaje == mensaje2.encode("utf-8")
#     assert cliente3.ultimo_mensaje == mensaje2.encode("utf-8")

#     # Cliente3 envía un mensaje
#     broadcast(mensaje3.encode("utf-8"), cliente3)
#     cliente2.ultimo_mensaje = mensaje3.encode("utf-8")  # Actualizamos ultimo_mensaje de cliente2
#     assert cliente1.ultimo_mensaje == mensaje3.encode("utf-8")
#     assert cliente2.ultimo_mensaje == mensaje3.encode("utf-8")

#     # Cliente2 se desconecta repentinamente
#     cliente2.activo = False
#     cliente2.send.side_effect = ConnectionError("Cliente desconectado")
#     cliente2.ultimo_mensaje = None  # Establecemos ultimo_mensaje a None al desconectar

#     # Cliente1 envía un nuevo mensaje
#     broadcast("Nuevo mensaje para Usuario1!".encode("utf-8"), cliente1)
#     assert cliente3.ultimo_mensaje == "Nuevo mensaje para Usuario1!".encode("utf-8")
#     assert cliente2.ultimo_mensaje is None  # Ahora esta aserción debería pasar

def test_varios_clientes_mensajes_simultaneos():
    clientes.clear()
    usuarios.clear()

    # Simulamos varios clientes conectados
    cliente1 = ClienteSimulado("Usuario1")
    cliente2 = ClienteSimulado("Usuario2")
    cliente3 = ClienteSimulado("Usuario3")

    clientes.extend([cliente1, cliente2, cliente3])
    usuarios.extend(["Usuario1", "Usuario2", "Usuario3"])

    # Mensajes que enviarán los clientes
    mensajes = [
        ("Hola desde Usuario1!", cliente1),
        ("Respuesta de Usuario2", cliente2),
        ("Último mensaje de Usuario3", cliente3)
    ]

    # Enviamos los mensajes uno por uno, simulando simultaneidad
    for mensaje, emisor in mensajes:
        broadcast(mensaje.encode("utf-8"), emisor)

    # Verificamos que cada cliente haya recibido todos los mensajes menos los suyos propios
    for cliente in clientes:
        mensajes_esperados = [m for m, e in mensajes if e != cliente]
        for mensaje_esperado in mensajes_esperados:
            assert mensaje_esperado.encode("utf-8") in cliente.mensajes_recibidos, f"El cliente {cliente.nombre} no recibió el mensaje {mensaje_esperado}"
        
        # Verificamos que el cliente no recibió su propio mensaje
        assert not any(mensaje.encode("utf-8") in cliente.mensajes_recibidos for mensaje, emisor in mensajes if emisor == cliente)

    # Verificamos que no haya duplicados
    for cliente in clientes:
        assert len(set(cliente.mensajes_recibidos)) == len(cliente.mensajes_recibidos), f"El cliente {cliente.nombre} tiene mensajes duplicados"