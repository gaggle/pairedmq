class PairedmqError(Exception):
    pass


class ClientError(PairedmqError):
    pass


class TimeoutError(PairedmqError):
    pass


OK = 200


class ServerError(PairedmqError):
    code = 500


class BadRequestError(ServerError):
    code = 400


class MethodNotAllowed(ServerError):
    code = 405
