import pytest
from server import ChatServer

@pytest.fixture 
def servidor_tdd(): 
    return ChatServer()

@pytest.mark.parametrize("mensaje_invalido", ["", "   "])
def test_validar_mensaje_vacio_falla(servidor_tdd, mensaje_invalido):
    # Fase Red: Esperamos que el método rechace strings vacíos o con puros espacios
    assert servidor_tdd.validar_mensaje(mensaje_invalido) is False

def test_validar_mensaje_valido_pasa(servidor_tdd):
    # Fase Red: Esperamos que el mismo método acepte texto válido
    assert servidor_tdd.validar_mensaje("Hola equipo") is True