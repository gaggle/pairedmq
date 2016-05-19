from appmq import mixins
from appmq.client import Client as _Client


class EvalExecClient(_Client, mixins.EvalExecMixin):
    def _launch_command(self, handshake_port):
        return ["python", "-c", "from evalexec.server import Server as S; S.create(%s)" % handshake_port]
