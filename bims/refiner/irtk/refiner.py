import logging
from typing import List, Optional

from .parser.parser import Parser
from .translator import Translator
from .policy import Policy
from .incompleteIntentException import IncompleteIntentException

LOGGER = logging.getLogger(__name__)

TRANSLATOR = Translator()


def refine(raw_intent: str) -> Optional[List[Policy]]:
    """Parses an intent. If it is a valid intent it also translates the parsed intent into a list
    of low-level policies and returns them.
    """
    parser = Parser()
    intent = parser.parse(raw_intent)

    if not intent:
        LOGGER.warning("Refiner: could not refine incomplete or invalid intent")
        raise IncompleteIntentException("Intent is incomplete",
                                        set(parser._state._transitions))

    policies = TRANSLATOR.translate(intent)
    return policies
