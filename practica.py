# Ejercicio 1: El Validador Estricto (pytest.raises y Fixtures)
import pytest
# # Tienes una clase que controla el ingreso de medidas de piezas de ensamblaje. Si la medida es negativa o igual a cero, debe rechazarla violentamente.

# Pseudocódigo (control_calidad.py):

from unittest.mock import patch

# Python
class Inspector:
    def verificar_medida(self, medida):
       # Si medida <= 0: lanzar ValueError con texto "Medida inválida"
     if medida <= 0:
         raise ValueError("Medida invalida")
      # Si no, retornar True
     else:
        return True

# Tu tarea: Crea un archivo de prueba. Usa un fixture para instanciar al Inspector y escribe dos pruebas: una para el caso de éxito (medida válida) y otra usando pytest.raises para capturar el error exacto cuando se envía un 0.
@pytest.fixture
def inspector_base():
   return Inspector()

def test_medida_valida(inspector_base):
   resultado = inspector_base.verificar_medida(15.5)
   assert resultado is True

def test_medida_invalida(inspector_base):
   with pytest.raises(ValueError,match= "Medida invalida"):
      inspector_base.verificar_medida(0)

# Ejercicio 2: El Notificador Multipropósito (parametrize y capsys)
# Tienes una función que recibe un nivel de alerta y un mensaje, y lo imprime en la consola con un formato específico.

# Pseudocódigo (alertas.py):

def emitir_alerta(nivel, mensaje):
    # Si nivel es "INFO": imprimir "[INFO] - mensaje"
    if nivel == "INFO":
       print(f'[INFO] - {mensaje}')
    # Si nivel es "ERROR": imprimir "[ERROR] - mensaje"
    if nivel == "ERROR":
       print(f'[ERROR] - {mensaje}')
    else:
        print(f'!!! CRITICO !!! - {mensaje}')
        
    # Si nivel es "CRITICO": imprimir "!!! CRITICO !!! - mensaje"


# Tu tarea: Escribe una sola prueba usando @pytest.mark.parametrize para evaluar los tres caminos posibles, y utiliza el fixture capsys para verificar que el print() está escupiendo el formato correcto en la consola.


@pytest.mark.parametrize("nivel,mensaje, resultado", [
   ("INFO", "Sistema listo", "[INFO] - Sistema listo\n"),
    ("ERROR", "Falla de red", "[ERROR] - Falla de red\n"),
    ("CRITICO", "Fuego detectado", "!!! CRITICO !!! - Fuego detectado\n")])
def test_niveles_alerta(nivel, mensaje, resultado, capsys):
   emitir_alerta(nivel, mensaje)
   alerta = capsys.readouterr()

   assert alerta == resultado


# Ejercicio 3: El Congelador del Tiempo (patch / Mocking)
# Tienes un script que intenta encender un motor. Si falla, espera 2 segundos e intenta de nuevo, hasta un máximo de 3 veces.

# Pseudocódigo (motor.py):

import time

class Motor:
    def arrancar_hardware(self):
        # Retorna False simulando que el hardware no responde
        return False

    def encender_con_reintentos(self):
        intentos = 0
        # Bucle de 3 intentos:
        while intentos < 3:
           if self.arrancar_hardware() == True:
              return "Encendido"
           else:
              print("Fallo al arrancar")
              intentos += 1
              time.sleep(2)
        return "Motor averiado"
        #   Si arrancar_hardware() es True: retornar "Encendido"
        #   Si es False: imprimir "Fallo al arrancar", hacer time.sleep(2)
        # Si terminan los 3 intentos: retornar "Motor averiado"


# Tu tarea: Escribe una prueba para el caso negativo total (el motor nunca arranca). Usa @patch para interceptar time.sleep (para que el test no tarde 6 segundos) y @patch.object para forzar a que arrancar_hardware siempre devuelva False. Verifica matemáticamente cuántas veces se llamó al sleep.

@patch('motor.time.sleep')
@patch.object(Motor, 'arrancar_hardware', return_value=False)
def test_fallo_total(mock_arrancar, mock_sleep, capsys):
   motor = Motor()
   resultado = motor.encender_con_reintentos()
   consola = capsys.readouterr()

   assert mock_arrancar.call_count == 3
   assert mock_sleep.call_count == 3

   assert "Fallo al arrancar" == consola.out
   assert resultado == "Motor averiado"

# Ejercicio 1: La Billetera Digital
# Estás desarrollando un sistema de pagos. Una billetera virtual tiene un saldo inicial y un método para gastar dinero.

# Pseudocódigo (billetera.py):

class Billetera:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def gastar(self, monto):
        # Si el monto es mayor al saldo actual, o es menor/igual a 0:
        if monto > self.saldo or monto <= 0:
           raise ValueError("Saldo insuficiente o monto invalido")
        #   Debe fallar reportando un error de tipo ValueError.
        # Si no, descuenta el monto del saldo y retorna el saldo restante.

        self.saldo -= monto
        return self.saldo


# Tu tarea: Escribe las pruebas necesarias para asegurar que una compra válida actualiza correctamente el saldo, y que intentar gastar más de lo disponible (o montos inválidos) provoca un fallo controlado por el sistema.

def test_compra_valida():
   billetera = Billetera(20000)
   billetera.gastar(5000)
   saldo_restante = 15000

   assert billetera.saldo == saldo_restante


def test_compra_invalida(saldo = 10000, monto = 3000000):
   billetera = Billetera(saldo)
   with pytest.raises(ValueError, match="Saldo insuficiente"):
    billetera.gastar(monto)


# Ejercicio 2: El Cotizador de Envíos
# Una empresa de logística necesita calcular el costo de envío de un paquete según el destino.

# Pseudocódigo (envios.py):

def calcular_envio(destino, peso_kg):
    # Si destino es "LOCAL": costo es peso_kg * 2
    if destino == "LOCAL":
       costo = peso_kg * 2
    # Si destino es "NACIONAL": costo es peso_kg * 5
    elif destino == "NACIONAL":
       costo = peso_kg * 5
    # Si destino es "INTERNACIONAL": costo es peso_kg * 12
    elif destino == "INTERNACIONAL":
       costo = peso_kg * 12
    # Para cualquier otro destino, debe fallar con un ValueError("Destino no soportado").
    else:
       raise ValueError("Destino no soportado")
    return costo

# Tu tarea: Escribe pruebas para verificar el cálculo correcto de los tres destinos válidos y el manejo del error para destinos inválidos, evitando al máximo la duplicación de código en tus pruebas.

@pytest.mark.parametrize("destino, peso_kg, resultado", [("LOCAL", 10, 20), ("NACIONAL", 3, 15), ("INTERNACIONAL", 3, 36)])
def test_destinos_validos(destino, peso_kg, resultado):
   costo_final = calcular_envio(destino, peso_kg)
   assert costo_final == resultado

def test_destino_invalido():
   with pytest.raises(ValueError, match="Destino no soportado"):
      calcular_envio("Paraguari", 3)

# Ejercicio 3: El Verificador de Estado de Servidor
# Un sistema cliente necesita consultar el estado de un servidor remoto. Hacer esta consulta real a través de internet toma 5 segundos y puede fallar si la red se cae.

# Pseudocódigo (monitor.py):

import time

class MonitorServidor:
    def consultar_red_externa(self):
        # Imagina que esto hace una llamada real a internet que tarda 5 segundos
        time.sleep(5)
        return "ONLINE"

    def verificar_sistema(self):
        # Llama a consultar_red_externa()
        estado = self.consultar_red_externa()
        if estado == "ONLINE":
            return "Sistema Operativo"
        else:
            return "Sistema Caído"
    
# Tu tarea: Escribe una prueba para verificar_sistema que se ejecute instantáneamente (sin esperar 5 segundos) y que simule tanto una respuesta exitosa ("ONLINE") como una respuesta de caída del servidor remoto.

@patch('monitor.time.sleep')
@patch.object(MonitorServidor, "consultar_red_externa", return_value="ONLINE")
def test_verif_sist(mock_consulta, mock_sleep):
   monitor = MonitorServidor()
   resultado = monitor.verificar_sistema()

   assert resultado == "Sistema Operativo"
   assert mock_sleep.call_count == 1


@patch('monitor.time.sleep')
@patch.object(MonitorServidor, "consultar_red_externa", return_value="OFFLINE")
def test_malo(mock_consulta, mock_sleep):
   monitor = MonitorServidor()
   resultado = monitor.verificar_sistema()

   assert resultado == "Sistema Caído"

