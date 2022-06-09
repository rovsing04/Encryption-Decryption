import os

from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_msg(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    enrypted_messsage = f.encrypt(encoded_message)

    print(enrypted_messsage)

def decrypt_msg(message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(message)

    print(decrypted_message)

def encrypt_file(filedir):
    key = load_key()
    f = Fernet(key)

    with open(filedir, 'rb') as file:
        original = file.read()

    encrypted = f.encrypt(original)

    with open(filedir, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(filedir):
    key = load_key()
    f = Fernet(key)

    with open(filedir, 'rb') as file:
        original = file.read()

    encrypted = f.decrypt(original)

    with open(filedir, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def encrypt_image(filedir, ext):
    fin = open(filedir, 'rb')
    # storing image data in variable "image"
    image = fin.read()
    fin.close()
    # converting image into byte array to perform decryption easily on numeric data
    image = bytearray(image)

    for index, values in enumerate(image):
        image[index] = values
    name = filedir.replace(ext, "")

    fin = open(f'{name}.txt', 'wb')
    fin.write(image)
    fin.close()
    os.remove(filedir)

    encrypt_file(f'{name}.txt')


def decrypt_image(filedir, ext):
    name = filedir.replace(ext, "")
    decrypt_file(f'{name}.txt')
    os.rename(f'{name}.txt', f'{name}{ext}')

