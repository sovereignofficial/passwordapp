from cryptography.fernet import Fernet
import os
import ast

class Encryptor:
    cryptoKey = None

    @staticmethod
    def generate_crypto_key():
        Encryptor.cryptoKey = Fernet.generate_key()
        with open("mykey.key", "wb") as f:
            f.write(Encryptor.cryptoKey)
    @staticmethod
    def load_crypto_key():
        if not os.path.exists("mykey.key"):
           Encryptor.generate_crypto_key()

        with open("mykey.key","rb") as f:
            Encryptor.cryptoKey = f.read()
            # Encryptor.cryptoKey = base64.urlsafe_b64decode(stored_key)

        return  Encryptor.cryptoKey

    @staticmethod
    def encrypt(password , key):
         fer = Fernet(key)
         secure_pass = fer.encrypt(password.encode())
         return secure_pass
    @staticmethod
    def decrypt(encrypted , key):
        fer = Fernet(key)
        parsed_val = ast.literal_eval(encrypted)
        decrypted_val= fer.decrypt(parsed_val)
        actual_pas = decrypted_val.decode()
        return actual_pas
    @staticmethod
    def compare_secure_keys(input,stored_val,key):
        correct_pass = Encryptor.decrypt(stored_val,key)
        return input == correct_pass

