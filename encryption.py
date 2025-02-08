from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
import os

# Load RSA Keys
def load_rsa_keys():
    with open("keys/private.pem", "rb") as priv_file:
        private_key = serialization.load_pem_private_key(
            priv_file.read(),
            password=None
        )

    with open("keys/public.pem", "rb") as pub_file:
        public_key = serialization.load_pem_public_key(pub_file.read())

    return private_key, public_key

private_key, public_key = load_rsa_keys()

# AES Encryption
def encrypt_rating(rating, aes_key):
    if not rating or not aes_key:
        print("ERROR: Missing rating or AES key")
        return None
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # Pad rating to 16 bytes
    rating_bytes = str(rating).encode()
    padding_length = 16 - (len(rating_bytes) % 16)
    padded_rating = rating_bytes + bytes([padding_length] * padding_length)

    encrypted_rating = encryptor.update(padded_rating) + encryptor.finalize()
    return iv + encrypted_rating  # Store IV with encrypted data

def decrypt_rating(encrypted_rating, aes_key):
    iv = encrypted_rating[:16]
    encrypted_data = encrypted_rating[16:]

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data[:-decrypted_data[-1]].decode()

# Encrypt AES Key using RSA
def encrypt_aes_key(aes_key):
    if not aes_key:
        print("ERROR: Missing AES key")
        return None
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Decrypt AES Key using RSA
def decrypt_aes_key(encrypted_aes_key):
    return private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
