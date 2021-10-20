from requests import Response


class PostFailedException(Exception):
    """
    A PostFailedException: Failure to post a request to an external endpoint.
    Note: This is related to the action of the post itself i.e. an invalid response should not utilize this exception.
    """

    def __init__(self, message: str, response: Response):
        self.message: str = message
        self.response: Response = response


class UnparsableException(Exception):
    """
    A UnparsableException: Failure to parse the provided data
    """

    def __init__(self, message: str):
        self.message: str = message
