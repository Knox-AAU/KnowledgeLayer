class PostFailedException(Exception):
    """
    A PostFailedException: Failure to post a request to an external endpoint.
    Note: This is related to the action of the post itself i.e. an invalid response should not utilize this exception.
    """
    def __init__(self, message, response):
        super().__init__(message)
        self.response = response

class UnparsableException(Exception):
    """
    A UnparsableException: Failure to parse the provided data
    """
    def __init__(self, message):
        super().__init__(message)