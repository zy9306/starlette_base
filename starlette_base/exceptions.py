class HTTPError(Exception):
    def __init__(self, status_code=400, message=""):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
