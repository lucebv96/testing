import pytest
from servidor_chat import broadcast, clientes

# Clase Cliente simulada para las pruebas
class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ultimo_mensaje = None

    def send(self, mensaje):
        self.ultimo_mensaje = mensaje

# Prueba para verificar que broadcast envía mensajes a todos excepto al emisor
def test_broadcast_envia_mensaje_a_todos_excep_al_emisor():
    # Limpiamos la lista global de clientes antes de iniciar
    clientes.clear()

    # Creamos algunos clientes simulados
    cliente1 = Cliente("Usuario1")
    cliente2 = Cliente("Usuario2")
    cliente3 = Cliente("Usuario3")

    # Añadimos los clientes a la lista global del servidor
    clientes.extend([cliente1, cliente2, cliente3])

    # El mensaje que queremos enviar
    mensaje = "Hola a todos!"

    # Enviamos el mensaje, simulando que cliente1 lo envió
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Verificamos que los otros clientes recibieron el mensaje
    assert cliente2.ultimo_mensaje == mensaje.encode("utf-8")
    assert cliente3.ultimo_mensaje == mensaje.encode("utf-8")

    # Verificamos que el cliente que envió el mensaje no lo recibió
    assert cliente1.ultimo_mensaje is None



def test_broadcast_no_envia_mensaje_vacio():
    clientes.clear()

    cliente1 = Cliente("Usuario1")
    cliente2 = Cliente("Usuario2")

    clientes.extend([cliente1, cliente2])

    mensaje = ""  # Mensaje vacío
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Ningún cliente debe recibir un mensaje vacío
    assert cliente2.ultimo_mensaje is None
    assert cliente1.ultimo_mensaje is None



def test_broadcast_mensaje_demasiado_largo():
    clientes.clear()

    cliente1 = Cliente("Usuario1")
    cliente2 = Cliente("Usuario2")

    clientes.extend([cliente1, cliente2])

    mensaje = "A" * 200  # Mensaje de 200 caracteres (límite ficticio de 128 bytes)
    broadcast(mensaje.encode("utf-8"), cliente1)

    # Los clientes no deben recibir un mensaje demasiado largo
    assert cliente2.ultimo_mensaje is None
    assert cliente1.ultimo_mensaje is None
