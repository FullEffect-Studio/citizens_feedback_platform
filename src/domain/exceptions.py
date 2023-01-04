class HttpException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict(())
        rv['message'] = self.message
        return rv


class UnauthorizedException(Exception):
    def __init__(self, message='Unauthorized access'):
        Exception.__init__(self)
        self.message = message
        self.status_code = 403

    def to_dict(self):
        rv = dict(())
        rv['message'] = self.message
        return rv


class BadRequestException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
        self.status_code = 400

    def to_dict(self):
        rv = dict(())
        rv['message'] = self.message
        return rv
