class EvalExecMixin(object):
    def sendrecv(self, *args, **kwargs):
        raise NotImplementedError

    def eval(self, data, **kwargs):
        return self.sendrecv(("eval", data), **kwargs)

    def exec_(self, data, **kwargs):
        return self.sendrecv(("exec", data), **kwargs)
