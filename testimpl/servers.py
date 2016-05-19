import time

from appmq import exc
from appmq.server import Server


class ExecEvalServer(Server):
    @staticmethod
    def _eval(arg):
        return eval(arg, globals(), globals())

    @staticmethod
    def _exec(arg):
        exec arg in globals(), globals()

    def _process_message(self, data):
        try:
            func, arg = data
            if func == "exec":
                self._exec(arg)
                return
            elif func == "eval":
                return self._eval(arg)
            raise exc.MethodNotAllowed(func)
        except Exception as ex:
            raise exc.BadRequestError(ex)


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
