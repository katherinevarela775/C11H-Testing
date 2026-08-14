import socket
import threading


class ChatServer:
    """Servidor de chat basado en sockets TCP."""

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.clientes_conectados = {}
        self.server_socket = None
        self.running = False

    def manejar_cliente(self, socket_cliente, direccion):
        # Etapa inicial: la lógica de sesión llega en commits posteriores.
        socket_cliente.close()

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
