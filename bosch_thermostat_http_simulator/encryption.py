"""Encryption logic of Bosch thermostat."""
import base64
import hashlib
import binascii
import json

from pyaes import PADDING_NONE, AESModeOfOperationECB, Decrypter, Encrypter

BS = 16


class Encryption:
    """Encryption class."""

    def __init__(self, access_key, magic, password=None):
        """
        Initialize encryption.

        :param str access_key: Access key to Bosch thermostat.
            If no password specified assumed as ready key to encrypt.
        :param str password: Password created with Bosch app.
        """
        self._bs = BS
        if password and access_key:
            key_hash = hashlib.md5(bytearray(access_key, "utf8") + magic)
            password_hash = hashlib.md5(magic + bytearray(password, "utf8"))
            self._saved_key = key_hash.hexdigest() + password_hash.hexdigest()
            self._key = binascii.unhexlify(self._saved_key)
        elif access_key:
            self._saved_key = access_key
            self._key = binascii.unhexlify(self._saved_key)

    @property
    def key(self):
        """Return key to store in config entry."""
        return self._saved_key

    def json_decrypt(self, raw):
        if raw:
            return json.loads(self.decrypt(raw))
        return None

    def encrypt(self, raw):
        """Encrypt raw message."""
        if len(raw) % self._bs != 0:
            raw = self._pad(raw)
        cipher = Encrypter(AESModeOfOperationECB(self._key), padding=PADDING_NONE)
        ciphertext = cipher.feed(raw) + cipher.feed()
        return base64.b64encode(ciphertext)

    def decrypt(self, enc):
        """
        Decryption algorithm.

        Decrypt raw message only if length > 2.
        Padding is not working for lenght less than 2.
        """
        try:
            if enc and len(enc) > 2:
                enc = base64.b64decode(enc)
                if len(enc) % self._bs != 0:
                    enc = self._pad(enc)
                    print("added padding by ourselves")
                else:
                    print("padding already", len(enc) % self._bs)
                    print(enc)
                cipher = Decrypter(
                    AESModeOfOperationECB(self._key), padding=PADDING_NONE
                )
                decrypted = cipher.feed(enc) + cipher.feed()
                print(decrypted)
                return decrypted.decode("utf8").rstrip(chr(0))
            return "{}"
        except Exception as err:
            pass

    def _pad(self, _s):
        """Pad of encryption."""
        return _s + ((self._bs - len(_s) % self._bs) * chr(0))
