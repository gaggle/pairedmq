import abc
import json
import traceback

import zmq

from . import exc
from .lib.handshake import handshake_sender


class Server(object):
    __metaclass__ = abc.ABCMeta
    handshake_timeout = 10000

    def __init__(self, handshake_port):
        self.socket, self.appport = _create_socket()
        handshake_sender(handshake_port, self.appport, self.handshake_timeout)

    @classmethod
    def create(cls, handshake_port):
        return cls(handshake_port).listen()

    def listen(self):
        while True:
            received = self.socket.recv()
            try:
                try:
                    code = exc.OK
                    response = self._process_message(self._unpickle(received))
                except exc.ServerError as ex:
                    code = ex.code
                    response = _exc_str()
                pickled = self._pickle([code, response])
            except Exception:
                pickled = self._pickle([exc.ServerError.code, _exc_str()])
            self.socket.send(pickled)

    @abc.abstractmethod
    def _process_message(self, data):
        pass

    @classmethod
    def _pickle(cls, data):
        return json.dumps(data)

    @classmethod
    def _unpickle(cls, data):
        return json.loads(data)


def _create_socket():
    socket = zmq.Context().socket(zmq.REP)
    port = socket.bind_to_random_port("tcp://127.0.0.1")
    return socket, port


def _exc_str():
    return "".join(traceback.format_exc())
