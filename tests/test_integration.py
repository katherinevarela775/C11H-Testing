import pytest
import socket
import threading
import time
from server import ChatServer

# Fixtures avanzados

@pytest.fixture
def gestor_servidor():
    """Fábrica que levanta servidores y los apaga automáticamente al terminar."""
    servidores_activos = []
    hilos_activos = []

    def _iniciar_servidor(puerto):
        servidor = ChatServer(host='127.0.0.1', port=puerto)
        hilo = threading.Thread(target=servidor.iniciar_servidor, daemon=True)
        hilo.start()
        time.sleep(0.5) # para que un test no se conecte antes de tiempo
        servidores_activos.append(servidor)
        hilos_activos.append(hilo)
        return servidor

    # Entregamos la función a la prueba
    yield _iniciar_servidor

    # teardown autom. al terminar una prueba
    for servidor in servidores_activos:
        servidor.detener_servidor()
    for hilo in hilos_activos:
        hilo.join(timeout=1.0)

@pytest.fixture
def gestor_clientes():
    """Fábrica que crea sockets de red y los cierra automáticamente al terminar."""
    clientes_activos = []

    def _crear_cliente():
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientes_activos.append(c)
        return c

    # Entregamos la función a la prueba
    yield _crear_cliente

    # teardown automatico
    for c in clientes_activos:
        try:
            c.close()
        except Exception:
            pass


# Pruebas de Integracion

# Parametrización de Payload: Ejecuta esta prueba 3 veces con distintos textos para estresar el UTF-8
@pytest.mark.parametrize("payload_mensaje", [
    "¡Hola desde la prueba de integracion!",         # Texto normal
    "Mensaje con emojis 🚀😎👾",                     # Emojis
    "Caracteres raros: @#%&*()_+{}:<>?~`"           # Símbolos especiales
])
def test_integracion_envio_y_recepcion(gestor_servidor, gestor_clientes, payload_mensaje):
    gestor_servidor(5005)
    
    cliente_1 = gestor_clientes()
    cliente_2 = gestor_clientes()

    cliente_1.connect(('127.0.0.1', 5005))
    cliente_2.connect(('127.0.0.1', 5005))

    cliente_1.recv(1024) # ambos reciben la petic. de ingresar el username
    cliente_2.recv(1024)

    cliente_1.send("Usuario_A".encode('utf-8'))
    cliente_2.send("Usuario_B".encode('utf-8'))
    time.sleep(0.5) 
    
    cliente_1.recv(1024) # mensajes de aviso de conexion del otro usuario
    cliente_2.recv(1024) 

    # Inyectamos dinámicamente el payload
    cliente_1.send(payload_mensaje.encode('utf-8'))
    respuesta_usuario_b = cliente_2.recv(1024).decode('utf-8') # guardamos lo que recibe el cliente 2
    
    # Comprobamos que el mensaje inyectado se recibió correctamente
    assert f"Usuario_A: {payload_mensaje}" in respuesta_usuario_b


def test_desconexion_inesperada_cliente(gestor_servidor, gestor_clientes):
    gestor_servidor(5006) # mismo proceso que en el test anterior
    
    cliente_1 = gestor_clientes()
    cliente_2 = gestor_clientes()

    cliente_1.connect(('127.0.0.1', 5006))
    cliente_2.connect(('127.0.0.1', 5006))

    cliente_1.recv(1024)
    cliente_2.recv(1024)

    cliente_1.send("Usuario_A".encode('utf-8'))
    cliente_2.send("Usuario_B".encode('utf-8'))
    time.sleep(0.5)

    cliente_1.recv(1024) 
    cliente_2.recv(1024) 

    cliente_1.close() # desconexion abrupta
    time.sleep(0.5) 

    aviso_desconexion = cliente_2.recv(1024).decode('utf-8')
    assert "Usuario_A ha abandonado el chat" in aviso_desconexion

    cliente_2.send("/users".encode('utf-8')) # envia un comando
    respuesta_comando = cliente_2.recv(1024).decode('utf-8')

    # verif. que es el unico cliente conectado
    assert "Conectados: Usuario_B" in respuesta_comando

def test_desconexion_masiva_y_durante_transmision(gestor_servidor, gestor_clientes):
    gestor_servidor(5008)

    c1 = gestor_clientes()
    c2 = gestor_clientes()
    c3 = gestor_clientes()

    c1.connect(('127.0.0.1', 5008))
    c2.connect(('127.0.0.1', 5008))
    c3.connect(('127.0.0.1', 5008))

    for c, name in zip([c1, c2, c3], ["A", "B", "C"]):
        c.recv(1024)
        c.send(name.encode('utf-8'))
    time.sleep(0.5)

    # forzamos al servidor a enviar un mensaje de un user desconectado
    c1.send("Mi último aliento".encode('utf-8'))
    c1.close() 
    
    # desconexion masiva
    c2.close()
    time.sleep(0.5)

    c3.settimeout(0.5)

    try: # limpieza del buffer del cliente c
        while True: c3.recv(4096)
    except socket.timeout:
        pass
    c3.settimeout(2.0)

    c3.send("/users".encode('utf-8'))
    respuestas = c3.recv(4096).decode('utf-8')
    
    assert "Conectados: C" in respuestas # verificacion final