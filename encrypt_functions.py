import os
from cryptography.fernet import Fernet

img_ext = [".jpeg", ".jpg", ".png", ".gif", ".svg"]
doc_ext = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".py", ".txt"]


def generate_key(dir):
    key = Fernet.generate_key()
    with open(f"{dir}.key", "wb") as key_file:
        key_file.write(key)


def load_key(keydir):
    try:
        return open(keydir, "rb").read()
    except:
        print('Not a valid key!')


def encrypt_msg(message, keydir):
    try:
        key = load_key(keydir)
        encoded_message = message.encode()
        f = Fernet(key)
        enrypted_messsage = f.encrypt(encoded_message)
        print(enrypted_messsage)
    except Exception as e:
        print(e)
        pass


def decrypt_msg(message, keydir):
    try:
        key = load_key(keydir)
        f = Fernet(key)
        message = message.encode()
        decrypted_message = f.decrypt(message)
        print(decrypted_message)
    except Exception as e:
        print(e)
        pass


def encrypt_file(filedir, keydir):
    try:
        key = load_key(keydir)
        f = Fernet(key)

        with open(filedir, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open(filedir, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    except Exception as e:
        print(e)
        pass


def decrypt_file(filedir, keydir):
    try:
        key = load_key(keydir)
        f = Fernet(key)

        with open(filedir, 'rb') as file:
            original = file.read()

        encrypted = f.decrypt(original)

        with open(filedir, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    except Exception as e:
        print(e)
        pass


def encrypt_image(filedir, ext, keydir):
    try:
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
        encrypt_file(f'{name}.txt', keydir)
    except:
        pass


def decrypt_image(filedir, ext, keydir):
    try:
        file_name, file_ext = os.path.splitext(filedir)
        decrypt_file(f'{file_name}.txt', keydir)
        os.rename(f'{file_name}.txt', f'{file_name}{ext}')
    except:
        pass


def encrypt_folder(source_dir, keydir):
    try:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                file_name, file_ext = os.path.splitext(name)
                if file_ext in doc_ext:
                    # print(f'Tries: {name}')
                    try:
                        encrypt_file(entry.path, keydir)
                        print(f'Encrypted: {name}')
                    except Exception as e:
                        print(e)
                elif file_ext in img_ext:
                    # print(f'Tries: {name}')
                    try:
                        encrypt_image(entry.path, file_ext, keydir)
                        print(f'Encrypted: {name}')
                    except Exception as e:
                        print(e)
                else:
                    print(f'{name} does not have a supported extension!')
    except:
        pass


def decrypt_folder(source_dir, keydir):
    try:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                file_name, file_ext = os.path.splitext(name)
                if file_ext in doc_ext:
                    # print(f'Tries: {name}')
                    try:
                        decrypt_file(entry.path, keydir)
                        print(f'Decrypted: {name}')
                    except Exception as e:
                        print(e)
                elif file_ext in img_ext:
                    # print(f'Tries: {name}')
                    try:
                        decrypt_image(entry.path, '.png', keydir)
                        print(f'Decrypted: {name}')
                    except Exception as e:
                        print(e)
                else:
                    print(f'{name} does not have a supported extension!')
    except:
        pass


