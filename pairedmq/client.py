import abc
import atexit
import json
import subprocess

import psutil
import zmq

from . import exc
from .lib import client_tools as tools
from .lib.handshake import handshake_receiver


class Client(object):
    __metaclass__ = abc.ABCMeta
    handshake_timeout = 10000
    timeout = 1000

    def __init__(self):
        self.port = None
        self.process = None
        self.socket = None
        self.poller = None
        self.initialize()

    def initialize(self):
        if self.socket:
            self.socket.close()
        if self.process:
            self.process.terminate()
            self.process.wait()

        with handshake_receiver(timeout=self.handshake_timeout) as (port, wait):
            self.process = subprocess.Popen(self._launch_command(port), env=tools.getenv())

            atexit.register(_safe_kill, self.process)
            try:
                self.port = int(wait())
            except exc.TimeoutError:
                tools.kill(self.process)
                raise
        self.socket, self.poller = _create_socket(self.port)

    def sendrecv(self, data, **kwargs):
        try:
            received = self._sendrecv(self._pickle(data),
                                      timeout=kwargs.pop("timeout", self.timeout))
        except exc.TimeoutError:
            self._reconnect_connections()
            raise
        code, response = self._unpickle(received)

        if code == exc.OK:
            return response
        else:
            raise exc.ClientError(response)

    def _sendrecv(self, data, timeout=None):
        self.socket.send_string(data)

        if self.poller.poll(timeout):
            received = self.socket.recv_string()
        else:
            raise exc.TimeoutError(data)
        return received

    @abc.abstractmethod
    def _launch_command(self, handshake_port):
        """
        :param handshake_port: str
        :rtype: str
        """
        pass

    def _reconnect_connections(self):
        if hasattr(self, "socket"):
            del self.socket
        if hasattr(self, "poller"):
            del self.poller
        self.socket, self.poller = _create_socket(self.port)

    @classmethod
    def _pickle(cls, data):
        return json.dumps(data)

    @classmethod
    def _unpickle(cls, data):
        return json.loads(data)


def _create_socket(port):
    socket = zmq.Context().socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://127.0.0.1:%s" % port)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    return socket, poller


def _safe_kill(p):
    if psutil.pid_exists(p.pid):
        tools.kill(p)
