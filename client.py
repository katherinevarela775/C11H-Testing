import socket
import threading


class ChatClient:
    """Cliente de chat basado en sockets TCP."""

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def recibir_mensajes(self):
        while self.running:
            try:
                mensaje = self.socket.recv(1024).decode('utf-8')
                if mensaje:
                    print(f"\n{mensaje}")
                    print("> ", end="", flush=True)
                else:
                    break
            except socket.timeout:
                continue
            except Exception:
                break
        self.running = False

    def enviar_mensajes(self, input_func=input):
        while self.running:
            try:
                texto = input_func("> ")
                if not self.running:
                    break
                if texto.strip():
                    self.socket.send(texto.encode('utf-8'))
                    if texto == "/exit":
                        self.running = False
                        return False
            except Exception:
                self.running = False
                break
        return True

    def conectar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1.0)
        try:
            self.socket.connect((self.host, self.port))
            self.running = True
            return True
        except Exception:
            return False

    def desconectar(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
