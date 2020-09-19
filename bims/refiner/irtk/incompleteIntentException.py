class IncompleteIntentException(Exception):
    """Incomplete Intent error.
    If an intent is valid but incomplete, an IncompleteIntentException is raised.
    Used for text suggestions when creating an intent.
    """
    def __init__(self, message, expected):
        self.message = message
        self.expected = expected