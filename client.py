import socket


class ChatClient:
    """Cliente de chat basado en sockets TCP."""

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

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
