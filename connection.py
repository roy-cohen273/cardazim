import struct
import socket


class Connection:
    """Represents a connection using the following protocol:
    Before each message is sent, its length is sent as an uint32 in little endian.
    """

    def __init__(self, sock):
        """Creates a new connection using a given socket.
        Make sure the given socket is ready to send/receive data,
        otherwise a BrokenPipe exception will be raised when trying to send/receive messages.

        It is recommended not to use this method. Use `Connection.connect` or `Listener.accept` instead.
        """
        self.sock = sock

    def __repr__(self):
        my_host, my_port = self.sock.getsockname()
        remote_host, remote_port = self.sock.getpeername()
        return f'<Connection from {my_host}:{my_port} to {remote_host}:{remote_port}>'

    def send_message(self, message: bytes):
        """Send `message` through the connection."""
        message_len = len(message)
        message_len = struct.pack('<I', message_len)
        self.sock.sendall(message_len)
        self.sock.sendall(message)

    def receive_message(self) -> bytes:
        """Receive a message through the connection."""
        message_len, = struct.unpack('<I', recv_all(self.sock, 4))
        message = recv_all(self.sock, message_len)

        # make sure the other side isn't sending anymore data
        if len(self.sock.recv(1)) != 0:
            raise Exception('Received more data than expected')
        return message

    @classmethod
    def connect(cls, host, port):
        """Creates a new connection to address (host, port)."""
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def close(self):
        """Close the connection."""
        self.sock.close()

    def __enter__(self):
        self.sock.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.sock.__exit__(exc_type, exc_value, traceback)



def recv_all(sock, bufsize, flags=0):
    """Receive data from the socket.
    The return value is a bytes object representing the data received.
    The amount of data received is exactly bufsize.
    """
    result = b''
    while (length_diff := bufsize - len(result)) > 0:
        result += sock.recv(length_diff, flags)
    return result

