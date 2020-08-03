import logging
from typing import Optional

import nltk

from ..intent import Intent
from .state import ErrorState, ForState, IllegalTransitionError
from ..validation import ValidationError

LOGGER = logging.getLogger(__name__)


class Parser:
    """Intent Parser implemented as a State Machine."""

    def __init__(self) -> None:
        self._state = ForState()
        self._error_state = ErrorState()
        self._intent = Intent()

    @property
    def intent(self) -> Optional[Intent]:
        """Parsed intent of Parser.

        If the Parser is in an accepting state, it returns the parsed intent. Otherwise, the
        parsed intent is incomplete or invalid and None is returned.
        """
        if not self._state.accepting:
            LOGGER.warning(
                "%s: could not extract incomplete or invalid intent: %s is not an accepting state",
                self,
                self._state
            )
            return None
        return self._intent

    @intent.setter
    def intent(self, intent: Intent) -> None:
        self._intent = intent

    def parse(self, raw_intent: str) -> Optional[Intent]:
        """Incrementally parses a raw intent.

        First, tokenizes the raw intent and passes the the tokens to the current state of the
        Parser. In case an illegal transition or a validation error occurs, the Parser transitions
        to the error state. Finally, attempts to return the parsed intent.
        """
        tokens = nltk.word_tokenize(raw_intent.lower())
        for token in tokens:
            try:
                self._state = self._state.run(token, self._intent)
            except (IllegalTransitionError, ValidationError) as error:
                LOGGER.warning(error)
                self._state = self._error_state
                raise
        return self.intent

    def __str__(self) -> str:
        return self.__class__.__name__
