import os
import base64
import json
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

PASSWORD_FILE = 'passwords.json'
SALT_SIZE = 16
KEY_SIZE = 32  # 32 bytes = 256 bits
ITERATIONS = 100000

def get_salt():
    return os.urandom(SALT_SIZE)

def get_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(password, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return iv, encryptor.tag, encrypted_password

def decrypt(encrypted_password, key, iv, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_password) + decryptor.finalize()

def store_password(title, password, master_password):
    salt = get_salt()
    key = get_key(master_password, salt)
    iv, tag, encrypted_password = encrypt(password, key)
    entry = {
        'salt': base64.b64encode(salt).decode(),
        'iv': base64.b64encode(iv).decode(),
        'tag': base64.b64encode(tag).decode(),
        'password': base64.b64encode(encrypted_password).decode()
    }
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    data[title] = entry
    with open(PASSWORD_FILE, 'w') as f:
        json.dump(data, f)

def retrieve_password(title, master_password):
    with open(PASSWORD_FILE, 'r') as f:
        data = json.load(f)
    entry = data[title]
    salt = base64.b64decode(entry['salt'])
    key = get_key(master_password, salt)
    iv = base64.b64decode(entry['iv'])
    tag = base64.b64decode(entry['tag'])
    encrypted_password = base64.b64decode(entry['password'])
    decrypted_password = decrypt(encrypted_password, key, iv, tag).decode()
    return decrypted_password, entry['salt'], entry['password']

def list_passwords(master_password):
    with open(PASSWORD_FILE, 'r') as f:
        data = json.load(f)
    titles = data.keys()
    print("Stored passwords:")
    for title in titles:
        print(f"- {title}")

def delete_password(title, master_password):
    with open(PASSWORD_FILE, 'r') as f:
        data = json.load(f)
    if title in data:
        del data[title]
        with open(PASSWORD_FILE, 'w') as f:
            json.dump(data, f)
        print(f"Password for '{title}' deleted successfully.")
    else:
        print(f"No password found for title '{title}'.")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: password_manager.py [generate|retrieve|list|delete] [arguments]")
        return

    command = sys.argv[1]
    if command == 'generate' and len(sys.argv) == 4:
        title = sys.argv[2]
        password = sys.argv[3]
        master_password = getpass("Enter master password: ")
        store_password(title, password, master_password)
        print(f"Password for '{title}' stored successfully.")
    elif command == 'retrieve' and len(sys.argv) == 3:
        title = sys.argv[2]
        master_password = getpass("Enter master password: ")
        decrypted_password, salt, encrypted_password = retrieve_password(title, master_password)
        print(f"Password for '{title}': {decrypted_password}")
        print(f"Salt: {salt}")
        print(f"Encrypted password: {encrypted_password}")
    elif command == 'list':
        master_password = getpass("Enter master password: ")
        list_passwords(master_password)
    elif command == 'delete' and len(sys.argv) == 3:
        title = sys.argv[2]
        master_password = getpass("Enter master password: ")
        delete_password(title, master_password)
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w') as f:
            json.dump({}, f)
    main()

