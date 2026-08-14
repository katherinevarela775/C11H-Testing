import socket
import threading
import time
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000): # se ejecuta al crear un cliente
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def recibir_mensajes(self): # unit e integration
        while self.running: # mientres que el cliente este conectado
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

    def enviar_mensajes(self, input_func=input):# (unit) input_func --> simular inputs del teclado 
        while self.running:
            try:
                texto = input_func("> ")
                if not self.running:
                    break
                if texto.strip():
                    self.socket.send(texto.encode('utf-8'))
                    if texto == "/exit":
                        self.running = False
                        return False # salida voluntaria
            except Exception:
                self.running = False
                break
        return True # salida involuntaria (reintentos)

    def conectar(self): # unit 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1.0) # limite de operac. de red
        try:
            self.socket.connect((self.host, self.port))
            self.running = True
            return True
        except:
            return False

    def desconectar(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

    def iniciar_cliente(self): # unit (reintentos)
        intentos_maximos = 5
        reintentos = 0

        while reintentos < intentos_maximos and not self.running:
            if reintentos > 0:
                print(f"🔄 Reintentando ({reintentos}/{intentos_maximos})...")
            
            if self.conectar():
                print(" ¡Conectado!")
                print("\n" + "="*30)
                print(" COMANDOS: /exit | /users | /help")
                print("="*30 + "\n")
                
                threading.Thread(target=self.recibir_mensajes, daemon=True).start()
                error_de_red = self.enviar_mensajes()
                
                if not error_de_red:
                    self.desconectar()
                    break
            else:
                reintentos += 1
                time.sleep(3)
        
        print(" Aplicación finalizada.")

if __name__ == "__main__":
    cliente = ChatClient()
    try:
        cliente.iniciar_cliente()
    except KeyboardInterrupt:
        cliente.desconectar()
        sys.exit(0)