import copy
from typing import List, Optional, Set

from .config import MIN_TX_RATE, MAX_TX_COST, MIN_POPULARITY, MIN_STABILITY
from .database.repository import Repository
from .intent import Blockchain, Currency, Filter, Intent, Modifier, Profile, Timeframe
from .policy import CostProfile, Interval, Policy, Time
from .validation import ValidationError


class Translator:
    """Translator translates an intent into a set of low-level policies.

    A policy is created for every user that the intent is specified for. The intent is also
    validated as part of the translation. The same translator instance can be used to translate
    multiple intents.
    """

    _TIMEFRAME = {
        Timeframe.DAY: (Time.DAY_START, Time.NIGHT_START),
        Timeframe.NIGHT: (Time.NIGHT_START, Time.DAY_START),
        Timeframe.MORNING: (Time.DAY_START, Time.AFTERNOON_START),
        Timeframe.AFTERNOON: (Time.AFTERNOON_START, Time.NIGHT_START),
    }

    _PROFILE = {
        Profile.CHEAPEST: CostProfile.ECONOMIC,
        Profile.FASTEST: CostProfile.PERFORMANCE,
    }

    def __init__(self, repository: Optional[Repository] = None) -> None:
        self._repository = repository or Repository()
        self._policy = Policy()

    def translate(self, intent: Intent) -> List[Policy]:
        """Translates the intent into a set of low-level policies."""
        self._policy = Policy()
        self._translate_base(intent)
        if intent.filters:
            self._translate_filters(intent)
        if intent.modifiers:
            self._translate_modifiers(intent)
        policies = self._map_policy_to_users(intent.users)
        return policies

    def _translate_base(self, intent: Intent) -> None:
        if intent.profile:
            self._policy.cost_profile = self._PROFILE[intent.profile]
        if intent.timeframe:
            self._policy.timeframe_start, self._policy.timeframe_end = \
                self._TIMEFRAME[intent.timeframe]
        if intent.interval:
            self._policy.interval = Interval(intent.interval.value)
        if intent.threshold:
            if intent.currency and intent.currency is not Currency.USD:
                intent.threshold *= self._repository.find_conversion_rate(intent.currency)
            self._policy.threshold = intent.threshold
        if intent.blockchain:
            self._policy.blockchain_pool = {intent.blockchain}
        if intent.whitelist:
            self._policy.blockchain_pool = intent.whitelist
        if intent.blacklist:
            self._policy.blockchain_pool = {*Blockchain} - intent.blacklist
            if not self._policy.blockchain_pool:
                raise ValidationError("invalid policy: blockchain pool cannot be empty", [])

    def _translate_filters(self, intent: Intent) -> None:
        if Filter.PUBLIC in intent.filters:
            self._policy.blockchain_type = Filter.PUBLIC.value
        if Filter.PRIVATE in intent.filters:
            self._policy.blockchain_type = Filter.PRIVATE.value
        if Filter.FAST in intent.filters:
            self._policy.min_tx_rate = MIN_TX_RATE
        if Filter.CHEAP in intent.filters:
            self._policy.max_tx_cost = MAX_TX_COST
        if Filter.STABLE in intent.filters:
            self._policy.min_stability = MIN_STABILITY
        if Filter.POPULAR in intent.filters:
            self._policy.min_popularity = MIN_POPULARITY

    def _translate_modifiers(self, intent: Intent) -> None:
        if Modifier.SPLITTING in intent.modifiers:
            self._policy.split_txs = True
        if Modifier.ENCRYPTION in intent.modifiers:
            self._policy.encryption = True
        if Modifier.REDUNDANCY in intent.modifiers:
            self._policy.redundancy = True

    def _map_policy_to_users(self, users: Set[str]) -> List[Policy]:
        policies = []
        for user in users:
            policy = copy.deepcopy(self._policy)
            policy.user = user
            policies.append(policy)
        return policies
