import time

from pairedmq.evalexec.server import EvalExecServer as _EvalExecServer
from pairedmq.server import Server

EvalExecServer = _EvalExecServer


class SimpleServer(Server):
    def _process_message(self, data):
        return "Hodor!"


class SlowResponseServer(Server):
    def _process_message(self, data):
        if data.endswith("sec"):
            try:
                duration = float(data[0:-3])
            except ValueError:
                duration = 10
            time.sleep(duration)
        return "Hodor!"


class SlowStartupServer(Server):
    def __init__(self, handshake_port):
        time.sleep(10)
        super(SlowStartupServer, self).__init__(handshake_port)

    def _process_message(self, data):
        return data


class ShortHandshakeServer(Server):
    handshake_timeout = 10

    def _process_message(self, data):
        return data
