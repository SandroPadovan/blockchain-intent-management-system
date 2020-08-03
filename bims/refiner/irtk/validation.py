class ValidationError(Exception):
    """Intent validation error.

    If an intent is invalid a validation error is emitted. Instead of using the built-in
    ValueError, a custom error is not ambiguous.
    """
