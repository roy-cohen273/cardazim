from typing import Optional, Union
import hashlib
import itertools

from PIL import Image
from Crypto.Cipher import AES

from serialization import serialize_int, deserialize_int, assert_deserialization_finished, extract_and_remove_prefix


class CryptImage:
    """Represents an image that can be encrypted and decrypted."""
    def __init__(self, image: Image.Image, key_hash: Optional[bytes]):
        """Creates a new CryptImage from a given image (PIL.Image.Image) and key hash."""
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: str):
        """Creates a new CryptImage from a file."""
        with Image.open(path) as image:
            image.load()
        return cls(image, None)

    def show(self):
        """Show the image on screen."""
        self.image.show()

    @property
    def image_data(self) -> bytes:
        """Get raw image data as a bytes object"""
        return self.image.tobytes()

    @image_data.setter
    def image_data(self, data: bytes):
        """Set the raw image data."""
        self.image.frombytes(data)

    def save_image(self, path, format=None):
        """Save the image (without metadata) to a given path."""
        self.image.save(path, format)


    def encrypt(self, key: bytes):
        """Encrypt the image using the given key."""
        first_hash = hashlib.sha256(key).digest()
        self.key_hash = hashlib.sha256(first_hash).digest()
        cipher = AES.new(first_hash, AES.MODE_EAX, nonce=b'arazim')
        self.image_data = cipher.encrypt(self.image_data)
        
    def decrypt(self, key: bytes) -> bool:
        """Attempt to decrypt the image using the given key. Returns whether it was successful."""
        first_hash = hashlib.sha256(key).digest()
        if hashlib.sha256(first_hash).digest() != self.key_hash:
            return False
        cipher = AES.new(first_hash, AES.MODE_EAX, nonce=b'arazim')
        self.image_data = cipher.decrypt(self.image_data)
        self.key_hash = None
        return True

    def serialize(self) -> bytes:
        """Serialize the CryptImage into a bytes object."""
        buf = bytearray()
        serialize_int(buf, self.image.height)
        serialize_int(buf, self.image.width)
        buf.extend(self.image_data)
        buf.extend(b'\x00' * 32 if self.key_hash is None else self.key_hash)
        return bytes(buf)

    @classmethod
    def deserialize(cls, data: Union[bytes, bytearray]):
        """Deserialize a CryptImage from a bytes object or from a bytearray.
        When deserializing from a bytearray, the data is read from the begining of the bytearray
        and then deleted from it.
        """
        if not isinstance(data, bytearray):
            buf = bytearray(data)
            result = cls.deserialize(buf)
            assert_deserialization_finished(buf)
            return result
        
        buf = data

        height = deserialize_int(buf)
        width = deserialize_int(buf)

        image_data = extract_and_remove_prefix(buf, height * width * 3)
        image = Image.frombytes('RGB', (width, height), image_data)

        key_hash = extract_and_remove_prefix(buf, 32)
        if key_hash == b'\x00' * 32:
            key_hash = None

        return cls(image, key_hash)
