from pairedmq import mixins
from pairedmq.client import Client as _Client


class EvalExecClient(_Client, mixins.EvalExecMixin):
    def _launch_command(self, handshake_port):
        return ["python", "-c", "from evalexec.server import EvalExecServer as S; S.create(%s)" % handshake_port]
