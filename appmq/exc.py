class AppmqError(Exception):
    pass


class ClientError(AppmqError):
    pass


class TimeoutError(AppmqError):
    pass


OK = 200


class ServerError(AppmqError):
    code = 500


class BadRequestError(ServerError):
    code = 400


class MethodNotAllowed(ServerError):
    code = 405
