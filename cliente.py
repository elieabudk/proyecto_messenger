from cryptography.fernet import Fernet
import socket
import threading

# Dirección IP pública del servidor y puerto
SERVER_HOST = 'ip del servidor'
PORT = "tu puerto"

# Cargar la clave de cifrado una vez
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

def receive_messages(s):
    while True:
        try:
            data = s.recv(1024)
            if data:
                decrypted_message = cipher_suite.decrypt(data).decode()
                print('Recibido del servidor:', decrypted_message)
        except Exception as e:
            print(f"Error al recibir datos del servidor: {e}")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((SERVER_HOST, PORT))
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")
        exit(1)

    # Inicia un hilo para recibir mensajes del servidor
    threading.Thread(target=receive_messages, args=(s,)).start()

    while True:
        message = input('Mensaje: ')
        try:
            encrypted_message = cipher_suite.encrypt(message.encode())
            s.sendall(encrypted_message)
        except Exception as e:
            print(f"Error al enviar datos al servidor: {e}")
            break





