from cryptography.fernet import Fernet

# Generar una clave
key = Fernet.generate_key()

# Guardar la clave en un lugar seguro
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("encriptado con exito ")