from pairedmq.evalexec.client import EvalExecClient


class MayaClient(EvalExecClient):
    def __init__(self, exepath):
        self.exe = exepath
        super(MayaClient, self).__init__()

    def _launch_command(self, handshake_port):
        return [self.exe, "-c",
                "from pairedmq.evalexec.server import EvalExecServer; "
                "EvalExecServer.create(%s)" % handshake_port]
