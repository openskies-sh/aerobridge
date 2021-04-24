from cryptography.fernet import Fernet

class EncrpytionHelper():
    ''' A class to help with Encrpytoin / Decryption of secure data within Aerobridge '''

    def __init__(self, secret_key):
        self.f = Fernet(secret_key)

    def encrypt(self, message):
        encrypted = self.f.encrypt(message)
        return encrypted
        

    def decrypt(self, encrypted_data):
        """
        Given a message (byes) and key (bytes), it decrypts the message and returns it
        """
        
        decrypted_data = self.f.decrypt(encrypted_data)
        return decrypted_data
