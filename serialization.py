"""Util functions for serialization and deserialization."""

import struct


def serialize_int(buf: bytearray, i: int):
    """Serialize an int as an uint32 in little endian and append it to the buffer."""
    buf.extend(struct.pack('<I', i))

def deserialize_int(buf: bytearray) -> int:
    """Deserialize an int from an uint32 in little endian and remove it from the buffer."""
    i, = struct.unpack('<I', buf[:4])
    del buf[:4]
    return i

def serialize_bytes(buf: bytearray, data: bytes):
    """Serialize a bytes object and append it to the buffer."""
    serialize_int(buf, len(data))
    buf.extend(data)

def deserialize_bytes(buf: bytearray) -> bytes:
    """Deserialize a bytes object and remove it from the buffer."""
    i = deserialize_int(buf)
    result = buf[:i]
    del buf[:i]
    return bytes(result)

def serialize_string(buf: bytearray, s: str) -> bytes:
    """Serialize a string and append it to the buffer."""
    serialize_bytes(buf, s.encode())

def deserialize_string(buf: bytearray) -> str:
    """Deserialize a string and remove it from the buffer."""
    return deserialize_bytes(buf).decode()
