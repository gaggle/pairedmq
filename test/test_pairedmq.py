import subprocess
import time
import unittest

import mock

from pairedmq import exc
from pairedmq.client import Client as _Client
from pairedmq.evalexec.client import EvalExecClient
from pairedmq.lib.client_tools import mergeenv


class Client(_Client):
    def __init__(self, server=None, timeout=None, handshake_timeout=None):
        if server:
            self.server = server
        if timeout:
            self.timeout = timeout
        if handshake_timeout:
            self.handshake_timeout = handshake_timeout
        super(Client, self).__init__()

    def _launch_command(self, handshake_port):
        return ["python", "-c", "from testimpl.servers import %s as S; "
                                "S.create(%s);" % (self.server, handshake_port)]


class TestPairedmq(unittest.TestCase):
    def test_custom_methods(self):
        client = EvalExecClient()
        assert client.eval("1 + 1") == 2
        client.exec_("a = 1; b = 1; c = a + b")
        assert client.eval("c") == 2

    def test_client_handshake_times_out(self):
        with self.assertRaises(exc.TimeoutError):
            Client(server="SlowStartupServer", handshake_timeout=10)

    def test_client_handshake_timeout_kills_process(self):
        with mock.patch("pairedmq.lib.client_tools.kill") as kill:
            try:
                Client(server="SlowStartupServer", handshake_timeout=10)
            except exc.TimeoutError:
                pass
            assert kill.called is True

    def test_server_handshake_times_out(self):
        cmds = ["python", "-c", "from testimpl.servers import ShortHandshakeServer as S; "
                                "S.create(%s);" % 9999]
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=mergeenv())
        out, err = p.communicate()
        assert "TimeoutError" in str(err)

    def test_hodor(self):
        client = Client(server="SimpleServer")
        res = client.sendrecv("Hodor?")
        assert res == "Hodor!"

    def test_send_multiple_times(self):
        client = Client(server="SimpleServer")
        client.sendrecv("Hodor?")
        res = client.sendrecv("Hodor?")
        assert res == "Hodor!"

    def test_sendrecv_times_out(self):
        client = Client(server="SlowResponseServer", timeout=10)
        with self.assertRaises(exc.TimeoutError):
            client.sendrecv("0.5sec")

    def test_sendrecv_accepts_custom_timeout(self):
        client = Client(server="SlowResponseServer")
        with self.assertRaises(exc.TimeoutError):
            client.sendrecv("0.5sec", timeout=10)

    def test_sendrecv_after_timeout(self):
        client = Client(server="SlowResponseServer")

        with self.assertRaises(exc.TimeoutError):
            client.sendrecv("0.3sec", timeout=10)
        time.sleep(0.3)
        res = client.sendrecv("0sec", timeout=1000)
        assert res == "Hodor!"

    def test_server_can_be_reinitialized(self):
        client = Client(server="SimpleServer")
        p1 = client.process.pid
        client.process.terminate()
        client.initialize()
        p2 = client.process.pid
        assert p1 != p2
