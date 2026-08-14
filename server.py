import socket
import threading
from datetime import datetime


class ChatServer:
    """Servidor de chat basado en sockets TCP."""

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.clientes_conectados = {}
        self.server_socket = None
        self.running = False

    def formatear_mensaje(self, mensaje_texto):
        if not isinstance(mensaje_texto, str):
            raise ValueError("El mensaje debe ser una cadena de texto")
        if not mensaje_texto.strip():
            raise ValueError("El mensaje no puede estar vacío")

        tiempo = datetime.now().strftime("%H:%M:%S")
        return f"[{tiempo}] {mensaje_texto}"

    def validar_mensaje(self, mensaje):
        return bool(mensaje and mensaje.strip())

    def broadcast(self, mensaje_texto, socket_emisor=None):
        if not mensaje_texto:
            return

        try:
            mensaje_final = self.formatear_mensaje(mensaje_texto)
        except ValueError:
            return

        for socket_cliente in list(self.clientes_conectados.keys()):
            if socket_cliente != socket_emisor:
                try:
                    socket_cliente.send(mensaje_final.encode('utf-8'))
                except Exception:
                    self.remover_cliente(socket_cliente)

    def manejar_cliente(self, socket_cliente, direccion):
        try:
            socket_cliente.send("Escribe tu nombre de usuario: ".encode('utf-8'))
            nombre = socket_cliente.recv(1024).decode('utf-8').strip()

            if not nombre:
                nombre = f"Anonimo_{direccion[1]}"

            self.clientes_conectados[socket_cliente] = nombre
            self.broadcast(f"{nombre} se ha unido al chat!")

            while self.running:
                try:
                    datos = socket_cliente.recv(1024)
                    if not datos:
                        break
                    mensaje = datos.decode('utf-8').strip()

                    if self.validar_mensaje(mensaje):
                        self.broadcast(f"{nombre}: {mensaje}", socket_cliente)
                except socket.timeout:
                    continue
        except Exception:
            pass
        finally:
            self.remover_cliente(socket_cliente)

    def remover_cliente(self, socket_cliente):
        if socket_cliente in self.clientes_conectados:
            nombre = self.clientes_conectados[socket_cliente]
            del self.clientes_conectados[socket_cliente]
            try:
                socket_cliente.close()
            except Exception:
                pass
            self.broadcast(f"{nombre} ha abandonado el chat.")

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1.0)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.running = True
            print(f"Servidor iniciado en {self.host}:{self.port}")
            print("Presiona Ctrl+C para apagar el servidor.")

            while self.running:
                try:
                    cl_socket, cl_address = self.server_socket.accept()
                    cl_socket.settimeout(1.0)
                    thread = threading.Thread(target=self.manejar_cliente, args=(cl_socket, cl_address))
                    thread.daemon = True
                    thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nApagando...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.detener_servidor()

    def detener_servidor(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        for cliente in list(self.clientes_conectados.keys()):
            try:
                cliente.close()
            except Exception:
                pass
        self.clientes_conectados.clear()


if __name__ == "__main__":
    servidor = ChatServer()
    servidor.iniciar_servidor()
