from typing import Optional
import struct

from crypt_image import CryptImage
from serialization import serialize_string, deserialize_string, assert_deserialization_finished


class Card:
    """Represents a card."""
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: Optional[str]):
        """Creates a new Card from a given name, creator's name, image (CryptImage), riddle and answer."""
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return f'<Card name={self.name!r} creator={self.creator!r}>'

    def __str__(self):
        return (f'Card {self.name} by {self.creator}\n'
                f'  riddle: {self.riddle}\n'
                f'  solution: {self.solution or "unsolved"}')

    @classmethod
    def create_from_path(cls, name: str, creator: str, path: str, riddle: str, solution: Optional[str]):
        """Creates a new card from a given name, creator's name, path to image, riddle and answer."""
        return cls(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        """Serialize the Card into a bytes object."""
        buf = bytearray()
        serialize_string(buf, self.name)
        serialize_string(buf, self.creator)
        buf.extend(self.image.serialize())
        serialize_string(buf, self.riddle)
        return bytes(buf)

    @classmethod
    def deserialize(cls, data: bytes):
        """Deserialize a Card from a bytes object."""
        buf = bytearray(data)
        name = deserialize_string(buf)
        creator = deserialize_string(buf)
        image = CryptImage.deserialize(buf)
        riddle = deserialize_string(buf)
        assert_deserialization_finished(buf)
        return cls(name, creator, image, riddle, None)

    def encrypt(self):
        """Encypt the card's image using its solution."""
        self.image.encrypt(self.solution.encode())

    def solve(self, solution: str) -> bool:
        """Attempt to solve the card using the given solution.
        Returns whether this was successful.
        """
        if self.image.decrypt(solution.encode()):
            self.solution = solution
            return True
        return False

