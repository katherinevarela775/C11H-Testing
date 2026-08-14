import socket
import threading
from datetime import datetime

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000): # autom. al crear el server
        self.host = host
        self.port = port
        self.clientes_conectados = {}
        self.server_socket = None 
        self.running = False

    def formatear_mensaje(self, mensaje_texto): # func. critica - unit 
        if not isinstance(mensaje_texto, str):
            raise ValueError("El mensaje debe ser una cadena de texto")
        if not mensaje_texto.strip():
            raise ValueError("El mensaje no puede estar vacío")
            
        tiempo = datetime.now().strftime("%H:%M:%S") # hora actual
        return f"[{tiempo}] {mensaje_texto}"

   
    # DEMO TDD: CICLO RED - GREEN - REFACTOR (funcion critica - TDD)

    # RED (La prueba falla porque la función acepta todo, incluso vacíos)
    # def validar_mensaje(self, mensaje):
    #     return True

    # GREEN (La prueba pasa, pero el código es muy básico/redundante)
    # def validar_mensaje(self, mensaje):
    #     if mensaje == "":
    #         return False
    #     if mensaje == "   ":
    #         return False
    #     if not mensaje:
    #         return False
    #     return True

    # REFACTOR (La prueba sigue pasando y el código está optimizado)
    # Este es el código final en producción:
    def validar_mensaje(self, mensaje):
        return bool(mensaje and mensaje.strip())
    

    def broadcast(self, mensaje_texto, socket_emisor=None): # integration
        if not mensaje_texto: return
        
        try:
            mensaje_final = self.formatear_mensaje(mensaje_texto) 
        except ValueError:
            return # evitamos enviar mensajes corruptos
            
        for socket_cliente in list(self.clientes_conectados.keys()):
            if socket_cliente != socket_emisor:
                try:
                    socket_cliente.send(mensaje_final.encode('utf-8'))
                except:
                    self.remover_cliente(socket_cliente)

    def procesar_comando(self, mensaje, socket_cliente, nombre): # func. critica - unit
        if mensaje == "/exit":
            try:
                socket_cliente.send("Saliendo...".encode('utf-8'))
            except: pass
            return "salir"
        elif mensaje == "/help":
            try:
                socket_cliente.send("Comandos: /exit, /help, /users".encode('utf-8'))
            except: pass
            return "comando"
        elif mensaje == "/users":
            lista = ", ".join(self.clientes_conectados.values())
            try:
                socket_cliente.send(f"Conectados: {lista}".encode('utf-8'))
            except: pass
            return "comando"
        else:
            return "mensaje_normal"

    def manejar_cliente(self, socket_cliente, direccion): # integration
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

                    # Evaluamos qué acción tomar usando la función extraída
                    accion = self.procesar_comando(mensaje, socket_cliente, nombre)
                    
                    if accion == "salir":
                        break
                    elif accion == "mensaje_normal":
                        if self.validar_mensaje(mensaje):
                            self.broadcast(f"{nombre}: {mensaje}", socket_cliente)
                            
                except socket.timeout:
                    continue
        except Exception:
            pass
        finally:
            self.remover_cliente(socket_cliente)

    def remover_cliente(self, socket_cliente): # integration
        if socket_cliente in self.clientes_conectados:
            nombre = self.clientes_conectados[socket_cliente]
            del self.clientes_conectados[socket_cliente]
            try:
                socket_cliente.close()
            except:
                pass
            self.broadcast(f"{nombre} ha abandonado el chat.")

    def iniciar_servidor(self): # integration
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
            except:
                pass
        for cliente in list(self.clientes_conectados.keys()):
            try:
                cliente.close()
            except:
                pass
        self.clientes_conectados.clear()

if __name__ == "__main__":
    servidor = ChatServer()
    servidor.iniciar_servidor()