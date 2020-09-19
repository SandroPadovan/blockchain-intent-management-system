import abc
import logging
from typing import Mapping, Optional

from ..intent import Blockchain, Currency, Filter, Intent, Interval, Modifier, Profile, Timeframe
from ..validation import ValidationError

LOGGER = logging.getLogger(__name__)

Transitions = Mapping[str, "State"]


class IllegalTransitionError(Exception):
    """Illegal state transition error.

    If a state of the Parser state machine encounters an invalid token (a token for which no
    transition is defined) while parsing an intent, it raises an IllegalTransitionError.
    """
    def __init__(self, message, expected):
        self.message = message
        self.expected = expected


class State(abc.ABC):
    """Abstract base state.

    Defines interface and base implementation for all other states.
    """

    def __init__(self, transitions: Optional[Transitions] = None, accepting: bool = False) -> None:
        self.accepting = accepting
        self._transitions = transitions or {}

    def run(self, token: str, intent: Intent) -> "State":
        """Implementation of a generic run method.

        Generic implementation of a run method that is called for each encountered token. In case
        an invalid token is encountered an illegal transition error is raised. Otherwise, it returns
        the successor state.
        """
        del intent
        if token not in self._transitions:
            raise IllegalTransitionError(
                f"{self}: illegal transition: expected {set(self._transitions)}, got '{token}'",
                set(self._transitions)
            )
        return self._transitions[token]

    def __str__(self) -> str:
        return self.__class__.__name__


class ValidationState(State):
    """An extension of the abstract base state.

    Defines interface and base implementation for states that perform validation.
    """

    def run(self, token: str, intent: Intent) -> State:
        """Implementation of a generic run method with validation.

        Generic implementation of a run method that also performs validation. After calling the
        generic base implementation of the run method defined by the base state, it performs
        validation. If the validation succeeds, that is there is no validation error raised, then
        it returns the successor state.
        """
        successor_state = super().run(token, intent)
        self._validate(token, intent)
        return successor_state

    @abc.abstractmethod
    def _validate(self, token: str, intent: Intent) -> None:
        raise NotImplementedError


class ForState(State):
    """Initial state leads to the UserState."""

    def __init__(self) -> None:
        super().__init__(transitions={"for": UserState()})


class UserState(ValidationState):
    """User state, expects a username and leads to the InSelectState."""

    def run(self, token: str, intent: Intent) -> State:
        self._validate(token, intent)
        return InSelectState(self)

    def _validate(self, token: str, intent: Intent) -> None:
        # Validation?
        intent.users.add(token)


class InSelectState(State):
    """InSelectState leads back to the UserState, TheState or TheBlockchainState."""

    def __init__(self, user_state: UserState) -> None:
        super().__init__(transitions={
            **dict.fromkeys({"and", ","}, user_state),
            "in": TheState(),
            "select": TheBlockchainState(),
        })


class TheState(State):
    """TheState leads to the TimeframeState."""

    def __init__(self) -> None:
        super().__init__(transitions={"the": TimeframeState()})


class TimeframeState(ValidationState):
    """TimeframeState leads to the SelectState.

    Validates the timeframe. Only accepts tokens that are members of the Timeframe enum.
    """

    def __init__(self) -> None:
        super().__init__(transitions=dict.fromkeys(Timeframe.values(), SelectState()))

    def _validate(self, token: str, intent: Intent) -> None:
        intent.timeframe = Timeframe(token)


class SelectState(State):
    """SelectState leads to the TheBlockchainState."""

    def __init__(self) -> None:
        super().__init__(transitions={"select": TheBlockchainState()})


class TheBlockchainState(ValidationState):
    """TheBlockchainState leads to the WithUntilAsState.

    Validates the token, whether or not it is a member of the Blockchain enum.
    """

    def __init__(self) -> None:
        super().__init__(
            transitions={
                **dict.fromkeys(Blockchain.values(), WithUntilAsState()),
                "the": ProfileState(),
            }
        )

    def _validate(self, token: str, intent: Intent) -> None:
        if token in Blockchain.values():
            intent.blockchain = Blockchain(token)


class WithUntilAsState(State):
    """WithUntilAsState leads to the ModifierState, The2State, or the DefaultState."""

    def __init__(self) -> None:
        super().__init__(transitions={
            "with": ModifierState(),
            "until": The2State(),
            "as": DefaultState(),
        })


class ProfileState(ValidationState):
    """ProfileState leads to the FilterBlockchainState.

    Validates the token. Only accepts tokens that are members of the Profile enum.
    """

    def __init__(self) -> None:
        super().__init__(transitions=dict.fromkeys(Profile.values(), FilterBlockchainState()))

    def _validate(self, token: str, intent: Intent) -> None:
        intent.profile = Profile(token)


class FilterStateValidator:
    """FilterStateValidator performs validation for various FilterStates.

    Exclusions are filter options that have no effect with the specified profile. If an exclusion
    is encountered, the filter options is simply ignored.
    Conflicts are filter options that are mutually exclusive. If a conflict is encountered, a
    validation error is raised.
    """

    _CONFLICTS: Mapping[Filter, Filter] = {
        Filter.PRIVATE: Filter.PUBLIC,
        Filter.PUBLIC: Filter.PRIVATE,
    }

    _EXCLUSIONS: Mapping[Filter, Profile] = {
        Filter.CHEAP: Profile.CHEAPEST,
        Filter.FAST: Profile.FASTEST,
    }

    def validate(self, token: str, intent: Intent) -> None:
        """Implementation of the filter validation.

        Checks filter options for exclusions and conflicts and acts accordingly.
        """
        if token not in Filter.values():
            return
        filter_ = Filter(token)
        if filter_ in self._CONFLICTS and self._CONFLICTS[filter_] in intent.filters:
            raise ValidationError(
                f"{self}: validation error: filters '{token}' and "
                f"'{self._CONFLICTS[filter_].value}' are mutually exclusive"
            )
        if filter_ in self._EXCLUSIONS and self._EXCLUSIONS[filter_] is intent.profile:
            LOGGER.info(
                "%s: filter '%s' has no effect with profile '%s'",
                self,
                token,
                intent.profile.value,
            )
            return
        intent.filters.add(filter_)

    def __str__(self) -> str:
        return self.__class__.__name__


class FilterBlockchainState(ValidationState):
    """FilterBlockchainState leads to the BlockchainState or the FromExceptWithUntilAsState.

    Validates the token. Delegates the validation to the FilterValidator.
    """

    def __init__(self) -> None:
        super().__init__(
            transitions={
                **dict.fromkeys(Filter.values(), BlockchainState(FilterState())),
                "blockchain": FromExceptWithUntilAsState(),
            }
        )
        self._validator = FilterStateValidator()

    def _validate(self, token: str, intent: Intent) -> None:
        self._validator.validate(token, intent)


class FilterState(ValidationState):
    """FilterState leads to the BlockchainState.

    Validates the token. Delegates the validation to the FilterValidator.
    """

    def __init__(self) -> None:
        super().__init__(transitions=dict.fromkeys(Filter.values(), BlockchainState(self)))
        self._validator = FilterStateValidator()

    def _validate(self, token: str, intent: Intent) -> None:
        self._validator.validate(token, intent)


class BlockchainState(State):
    """BlockchainState leads to the FromExceptWithUntilAsState."""

    def __init__(self, filter_state: FilterState) -> None:
        super().__init__(transitions={
            **dict.fromkeys({"and", ","}, filter_state),
            "blockchain": FromExceptWithUntilAsState(),
        })


class FromExceptWithUntilAsState(State):
    """FromExceptWithUntilAsState leads to the White-, or BlacklistState, ModifierState,
    The2State, or DefaultState.
    """

    def __init__(self) -> None:
        super().__init__(transitions={
            "from": WhitelistState(),
            "except": BlacklistState(),
            "with": ModifierState(),
            "until": The2State(),
            "as": DefaultState(),
        })


class WhitelistState(ValidationState):
    """WhitelistState leads to the WhitelistWithUntilAsState.

    Validates the token. Only accepts tokens that are a member of the Blockchain enum.
    """

    def __init__(self) -> None:
        super().__init__(
            transitions=dict.fromkeys(Blockchain.values(), WhitelistWithUntilAsState(self)),
        )

    def _validate(self, token: str, intent: Intent) -> None:
        intent.whitelist.add(Blockchain(token))


class WhitelistWithUntilAsState(State):
    """WhitelistWithUntilAsState leads back to the WhitelistState, ModifierState, The2State, or
    DefaultState.
    """

    def __init__(self, whitelist_state: WhitelistState) -> None:
        super().__init__(transitions={
            **dict.fromkeys({"and", ","}, whitelist_state),
            "with": ModifierState(),
            "until": The2State(),
            "as": DefaultState(),
        })


class BlacklistState(ValidationState):
    """BlacklistState leads to the BlacklistWithUntilAsState.

    Validates the token. Only accepts tokens that are a member of the Blockchain enum.
    """

    def __init__(self) -> None:
        super().__init__(
            transitions=dict.fromkeys(Blockchain.values(), BlacklistWithUntilAsState(self)),
        )

    def _validate(self, token: str, intent: Intent) -> None:
        intent.blacklist.add(Blockchain(token))


class BlacklistWithUntilAsState(State):
    """BlacklistWithUntilAsState leads back to the BlacklistState, ModifierState, The2State, or
    DefaultState.
    """

    def __init__(self, blacklist_state: BlacklistState) -> None:
        super().__init__(transitions={
            **dict.fromkeys({"and", ","}, blacklist_state),
            "with": ModifierState(),
            "until": The2State(),
            "as": DefaultState(),
        })


class ModifierState(ValidationState):
    """ModifierState leads to the UntilAsState.

    Validates the token. Only accepts tokens that are a member of the Modifier enum.
    """

    def __init__(self) -> None:
        super().__init__(transitions=dict.fromkeys(Modifier.values(), UntilAsState(self)))

    def _validate(self, token: str, intent: Intent) -> None:
        intent.modifiers.add(Modifier(token))


class UntilAsState(State):
    """UntilAsState leads back to the ModifierState, The2State, or DefaultState."""

    def __init__(self, modifier_state: ModifierState) -> None:
        super().__init__(transitions={
            **dict.fromkeys({"and", ","}, modifier_state),
            "until": The2State(),
            "as": DefaultState(),
        })


class The2State(State):
    """The2State leads to the IntervalState."""

    def __init__(self) -> None:
        super().__init__(transitions={"the": IntervalState()})


class IntervalState(ValidationState):
    """IntervalState leads to the CostsState.

    Validates the token. Only accepts tokens that are a member of the Interval enum.
    """

    def __init__(self) -> None:
        super().__init__(transitions=dict.fromkeys(Interval.values(), CostsState()))

    def _validate(self, token: str, intent: Intent) -> None:
        intent.interval = Interval(token)


class CostsState(State):
    """CostsState leads to the ReachState."""

    def __init__(self) -> None:
        super().__init__(transitions={"costs": ReachState()})


class ReachState(State):
    """ReachState leads to the CurrencyThresholdState."""

    def __init__(self) -> None:
        super().__init__(transitions={"reach": CurrencyThresholdState()})


class CurrencyThresholdState(ValidationState):
    """CurrencyThresholdState leads to the ThresholdState or PolicyState.

    Validates the currency. The specification of a currency is optional and can be omitted. In
    case no currency is specified, the token is instead passed directly to the ThresholdState and
    the default currency (USD) is used.
    """

    def __init__(self) -> None:
        self._threshold_state = ThresholdState()
        super().__init__(transitions=dict.fromkeys(Currency.values(), self._threshold_state))

    def run(self, token: str, intent: Intent) -> State:
        """In case no currency is specified, the token is instead passed directly to the
        ThresholdState and the default currency (USD) is used.
        """
        if token not in self._transitions:
            # The currency of the cost threshold can be omitted. The default value is
            # 'Currency.USD'. In case the token is not a valid currency, it is forwarded to the
            # ThresholdState.
            return self._threshold_state.run(token, intent)
        self._validate(token, intent)
        return self._transitions[token]

    def _validate(self, token: str, intent: Intent) -> None:
        intent.currency = Currency(token)


class ThresholdState(ValidationState):
    """ThresholdState leads to the PolicyState.

    Validates the threshold, by attempting to convert it to a float.
    """

    def run(self, token: str, intent: Intent) -> State:
        """Validates the threshold. In case the token is not a float, a validation error is
        raised. Otherwise, the PolicyState is returned as successor state.
        """
        self._validate(token, intent)
        return PolicyState()

    def _validate(self, token: str, intent: Intent) -> None:
        try:
            intent.threshold = float(token)  # float("NaN") -> nan
        except ValueError as error:
            raise ValidationError(f"{self}: validation error: {error}")


class PolicyState(State):
    """PolicyState is an accepting state.

    If any token is encountered in this state, the error state is returned as successor state.
    """

    def __init__(self) -> None:
        # This is an accepting state representing a valid intent corresponding to a policy.
        # However, any input token received in this state, invalidates the intent and leads to the
        # ErrorState.
        super().__init__(accepting=True)


class DefaultState(ValidationState):
    """DefaultState leads to the DefaultPolicyState.

    Validates the intent, a default policy cannot specify a timeframe.
    """

    def __init__(self) -> None:
        # The default policy has to be validated before the DefaultPolicy state (accepting state) is
        # actually reached to be effective.
        super().__init__(transitions={"default": DefaultPolicyState()})

    def _validate(self, token: str, intent: Intent) -> None:
        if intent.timeframe:
            LOGGER.info("%s: timeframe has no effect in default policy", self)
            intent.timeframe = None


class DefaultPolicyState(State):
    """DefaultPolicyState is an accepting state.

    If any token is encountered in this state, the error state is returned as successor state.
    """

    def __init__(self) -> None:
        # This is an accepting state representing a valid intent corresponding to a default policy.
        # However, any input token received in this state, invalidates the intent and leads to the
        # ErrorState.
        super().__init__(accepting=True)


class ErrorState(State):
    """ErrorState is a special state that is reached if an error occurs during the parsing of the
    intent.

    The ErrorState does not define any outgoing transitions. Every token that is encountered leads
    back to this state.
    """

    def run(self, token: str, intent: Intent) -> State:
        del intent
        # This state acts as a sink. It does not define any outgoing links to other states.
        # Regardless of the input token, when run it always returns a reference to itself.
        # Therefore, once this state is reached, it cannot be left.
        return self
