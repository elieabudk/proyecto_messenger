import socket
import threading
from cryptography.fernet import Fernet





# Cargar la clave de cifrado
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Crear el objeto Fernet para cifrado y descifrado
cipher_suite = Fernet(key)

# Diccionario para almacenar las conexiones de los clientes
clientes = {}

# Función para manejar la conexión de un cliente
def handle_client(conn, addr):
    print(f'Conectado por {addr}')
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f'Cliente {addr} desconectado')
                    del clientes[addr]
                    break

                # Descifrar el mensaje recibido
                print(f'Recibido del cliente {addr}: {data}')  # Imprimir el mensaje encriptado

                # Reenviar el mensaje cifrado a todos los otros clientes
                for client_addr, client_conn in list(clientes.items()):
                    if client_addr != addr:
                        try:
                            client_conn.sendall(data)
                        except:
                            print(f'Error enviando a {client_addr}, eliminando cliente.')
                            del clientes[client_addr]
                            client_conn.close()

            except Exception as e:
                print(f'Error manejando el cliente {addr}: {e}')
                if addr in clientes:
                    del clientes[addr]
                break

# Dirección y puerto en los que el servidor escuchará
HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red disponibles
PORT = "tu puerto"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor escuchando en {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        clientes[addr] = conn  # Almacena la conexión del cliente
        threading.Thread(target=handle_client, args=(conn, addr)).start()

