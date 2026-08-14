import pytest
from unittest.mock import patch
from server import ChatServer
from client import ChatClient

# Inyeccion de dependencias
@pytest.fixture
def servidor_base():
    """Entrega un servidor nuevo y limpio automáticamente a las pruebas que lo pidan."""
    return ChatServer()

@pytest.fixture
def cliente_base():
    """Entrega un cliente nuevo y limpio automáticamente a las pruebas que lo pidan."""
    return ChatClient()

@pytest.fixture
def socket_falso():
    """Entrega un DummySocket base listo para usar."""
    return DummySocket()

class DummySocket: # Clase mock
    """Un socket falso (mock) para probar funciones de red de manera aislada."""
    def __init__(self, datos_a_recibir=b""):
        self.datos_a_recibir = datos_a_recibir
        self.datos_enviados = [] 

    def close(self):
        pass

    def send(self, data):
        self.datos_enviados.append(data) # se guarda en el historial para analizarlo despues

    def recv(self, bufsize):
        datos = self.datos_a_recibir
        self.datos_a_recibir = b"" # vaciamos la memoria para simular desconexion
        return datos
        
    def settimeout(self, tiempo): #ignora config. de tiempo para las pruebas rapidas
        pass

# Pruebas unitarias

def test_formatear_mensaje_positivo(servidor_base): # happy path 
    resultado = servidor_base.formatear_mensaje("Hola a todos")
    
    assert "Hola a todos" in resultado # verifica que el texto sea el mismo
    assert "[" in resultado and "]" in resultado # si se agg. los corchetes que envuelven la hora

def test_formatear_mensaje_negativo_vacio(servidor_base): # Caso Negativo
    with pytest.raises(ValueError, match="El mensaje no puede estar vacío"): # pytest atrapa el error
        servidor_base.formatear_mensaje("   ")

def test_conectar_negativo_ip_invalida(): # Caso Negativo
    # Comprobac. de como maneja el cliente el error
    cliente = ChatClient(host='256.256.256.256', port=99999) # ip inexistente y puerto invalido
    resultado = cliente.conectar()
    
    assert resultado is False # nos aseguramos que el cliente haya atrapado el error y devuelva un false, en vez de colapsar

def test_cliente_enviar_mensajes_normal(cliente_base, socket_falso):
    # Verificamos que un mensaje normal se envía por el socket
    cliente_base.running = True
    cliente_base.socket = socket_falso # reemplazamos el socket real por el falso inyectado
    
    # Simulamos que el usuario escribe un mensaje y luego sale
    entradas = ["Hola Servidor", "/exit"]

    def input_simulado(prompt): # input que simula el teclado
        return entradas.pop(0)
    
    cliente_base.enviar_mensajes(input_func=input_simulado)
    
    assert b"Hola Servidor" in cliente_base.socket.datos_enviados # comprobac. del historial del socket falso


def test_cliente_recibir_mensajes_positivo(capsys, cliente_base):
    # Verif. procesam. de los mensajes entrantes y se detiene si el servidor cae
    cliente_base.running = True

    # Simulamos que el servidor nos envía un "Ping" (Aquí instanciamos uno nuevo para pasarle el dato)
    cliente_base.socket = DummySocket(datos_a_recibir=b"Ping")
    
    # procesará "Ping" y luego devolverá b"", rompiendo el bucle
    cliente_base.recibir_mensajes()
    
    consola = capsys.readouterr() # lectura de la consola
    assert "Ping" in consola.out
    
    # Verif. la desconexión
    assert cliente_base.running is False

# pytest ejecutara esta funcion 4 veces con estos parametros
@pytest.mark.parametrize("comando_enviado, respuesta_esperada", [
    ("/help", "comando"),
    ("/users", "comando"),
    ("/exit", "salir"),
    ("Hola mundo", "mensaje_normal")
])
def test_procesar_comandos_rutas_completas(servidor_base, socket_falso, comando_enviado, respuesta_esperada): 
    # rutas de ejecución de comandos funcionen (Cobertura Completa)
    servidor_base.clientes_conectados[socket_falso] = "Usuario_Prueba" # usuario simulado para /users
    
    resultado = servidor_base.procesar_comando(comando_enviado, socket_falso, "Usuario_Prueba")
    assert resultado == respuesta_esperada

@patch("client.time.sleep") # para que el testeo sea rapido
@patch.object(ChatClient, "conectar", return_value=False) 
def test_cliente_reintentos_conexion(mock_conectar, mock_sleep, capsys, cliente_base): # caso negativo llega al limite y el cliente se rinde
    
    cliente_base.iniciar_cliente()
    
    # Capturamos la consola
    consola = capsys.readouterr()
    
    # Validaciones de comportamiento (Behavioral Testing)
    assert mock_conectar.call_count == 5 # Verif. que intento conectarse 5 veces
    assert mock_sleep.call_count == 5 # Verif. que llamó a time.sleep() 5 veces
    
    # Validaciones de experiencia de usuario (UX)
    assert "Reintentando (1/5)..." in consola.out
    assert "Reintentando (4/5)..." in consola.out
    assert "Aplicación finalizada." in consola.out # Verificamos que el programa no colapsó al rendirse