from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64


# AES Symmetric Encryption/Decryption
class SymmetricEncryption:
    def __init__(self, key=None):
        self.key = key or b'mysecurekey12345'  # Default key
        self.iv = os.urandom(16)

    def set_key(self, new_key):
        if len(new_key) not in (16, 24, 32):
            raise ValueError("AES key length must be 16, 24, or 32 bytes!")
        self.key = new_key

    def encrypt(self, plaintext):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv))
        encryptor = cipher.encryptor()
        return self.iv + encryptor.update(plaintext.encode())

    def decrypt(self, ciphertext):
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext[16:]).decode()
