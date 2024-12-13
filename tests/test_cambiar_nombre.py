import pytest
from unittest.mock import Mock  # Añade esta línea para importar Mock
from servidor_chat import cambiar_nombre, clientes, usuarios

def test_cambiar_nombre():
    # Limpiamos las listas para empezar con un estado conocido
    clientes.clear()
    usuarios.clear()

    # Simulamos un cliente
    cliente = Mock()
    clientes.append(cliente)
    usuarios.append("Usuario1")

    # Intentamos cambiar el nombre
    cambiar_nombre(cliente, "NuevoUsuario")

    # Verificamos que el nombre se haya cambiado en la lista de usuarios
    assert "NuevoUsuario" in usuarios
    assert "Usuario1" not in usuarios

    # Verificamos que el cliente haya recibido un mensaje de confirmación
    cliente.send.assert_called_once_with(b"Tu nombre ha sido cambiado a NuevoUsuario")