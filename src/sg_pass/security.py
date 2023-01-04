import secrets
from typing import Final

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.padding import PKCS7

PBKDF2_LENGTH: Final[int] = 32
PBKDF2_ITERATIONS: Final[int] = 1_000_000


class Security:

    def __init__(self, key_provider):
        self.provider = key_provider

    @staticmethod
    def __pbkdf2(salt: bytes) -> PBKDF2HMAC:
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=PBKDF2_LENGTH,
            iterations=PBKDF2_ITERATIONS,
            salt=salt
        )

    def __aes(self):
        return algorithms.AES(self.provider.get_key())

    def __pkcs7_pad(self) -> PKCS7:
        return padding.PKCS7(self.__aes().block_size)

    def get_derived_key(self, password: bytes, salt: bytes) -> bytes:
        return self.__pbkdf2(salt).derive(password)

    def validate_key(self, password: bytes, salt: bytes) -> bool:
        try:
            self.__pbkdf2(salt).verify(password, self.provider.get_key())
            return True
        except InvalidKey:
            return False

    def cipher_data(self, data: bytes) -> bytes:
        encryptor = Cipher(self.__aes(), modes.ECB()).encryptor()
        pad = self.__pkcs7_pad().padder()
        padded_data = pad.update(data) + pad.finalize()

        return encryptor.update(padded_data) + encryptor.finalize()

    def decipher_data(self, data: bytes) -> bytes:
        decryptor = Cipher(self.__aes(), modes.ECB()).decryptor()
        decrypted_text = decryptor.update(data) + decryptor.finalize()
        unpad = self.__pkcs7_pad().unpadder()

        return unpad.update(decrypted_text) + unpad.finalize()


def main():
    class KeyProvider:

        def __init__(self):
            self.password = secrets.token_hex(12).encode()
            self.salt = secrets.token_hex(4).encode()

            print(f"Password: {self.password.decode()}")
            print(f"Salt: {self.salt.decode()}")

            self.key = None

        def get_key(self):
            if self.key is None:
                self.key = Security(self).get_derived_key(self.password, self.salt)
            return self.key

    security = Security(KeyProvider())
    data = b"Lorem ipsum dolor sit amet"

    ciphered = security.cipher_data(data)
    deciphered = security.decipher_data(ciphered)

    print(f"{ciphered.hex()}")
    print(f"-> {deciphered.decode()}")


if __name__ == '__main__':
    main()
