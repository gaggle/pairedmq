from pairedmq import exc
from pairedmq.server import Server as _Server


class EvalExecServer(_Server):
    def _process_message(self, data):
        func, arg = data
        try:
            if func == "exec":
                self._exec(arg)
                return
            elif func == "eval":
                return self._eval(arg)
            raise exc.MethodNotAllowed(func)
        except Exception as ex:
            raise exc.BadRequestError(ex)

    @classmethod
    def _eval(cls, arg):
        return eval(arg, globals(), globals())

    @classmethod
    def _exec(cls, arg):
        exec arg in globals(), globals()
