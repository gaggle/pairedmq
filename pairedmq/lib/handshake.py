from contextlib import contextmanager

import zmq

from pairedmq.exc import TimeoutError


@contextmanager
def handshake_receiver(timeout=None):
    socket = zmq.Context().socket(zmq.REP)
    socket.setsockopt(zmq.LINGER, 0)
    port = socket.bind_to_random_port("tcp://127.0.0.1")

    def wait():
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        if poller.poll(timeout):
            received = int(socket.recv(zmq.DONTWAIT))
            socket.send_string("")  # Ack reception
        else:
            raise TimeoutError("Handshake timeout")
        return received

    yield (port, wait)
    socket.close()


def handshake_sender(handshake_port, port, timeout=None):
    if timeout is None:
        timeout = -1
    socket = zmq.Context().socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://127.0.0.1:%s" % handshake_port)
    socket.send_string(str(port))

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    if poller.poll(timeout):
        socket.recv()  # wait for ack
        socket.close()
    else:
        socket.close()
        raise TimeoutError("Handshake timeout")
