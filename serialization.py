"""Util functions for serialization and deserialization."""

import struct


def take(buf: bytearray, length: int) -> bytearray:
    """Take the first `length` bytes from `buf` and remove them from `buf`."""
    if len(buf) < length:
        raise ValueError('Not enough data')
    result = buf[:length]
    del buf[:length]
    return result

def serialize_int(buf: bytearray, i: int):
    """Serialize an int as an uint32 in little endian and append it to the buffer."""
    buf.extend(struct.pack('<I', i))

def deserialize_int(buf: bytearray) -> int:
    """Deserialize an int from an uint32 in little endian and remove it from the buffer."""
    i, = struct.unpack('<I', take(buf, 4))
    return i

def serialize_bytes(buf: bytearray, data: bytes):
    """Serialize a bytes object and append it to the buffer."""
    serialize_int(buf, len(data))
    buf.extend(data)

def deserialize_bytes(buf: bytearray) -> bytes:
    """Deserialize a bytes object and remove it from the buffer."""
    i = deserialize_int(buf)
    return bytes(take(buf, i))

def serialize_string(buf: bytearray, s: str) -> bytes:
    """Serialize a string and append it to the buffer."""
    serialize_bytes(buf, s.encode())

def deserialize_string(buf: bytearray) -> str:
    """Deserialize a string and remove it from the buffer."""
    return deserialize_bytes(buf).decode()

def assert_deserialization_finished(buf: bytearray):
    """Assert that the deserialization is finished, AKA the buffer is empty."""
    if buf:
        raise ValueError('Too much data')
