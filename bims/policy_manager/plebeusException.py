class PlebeusException(Exception):
    """Generic exception for an error from PleBeuS."""

    def __init__(self, message):
        self.message = message
