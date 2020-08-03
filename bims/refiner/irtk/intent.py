import dataclasses
from dataclasses import field
import enum
from typing import Iterable, Optional, Set


class AutoName(enum.Enum):
    """Base enum that automatically sets the value based on the member name."""

    @classmethod
    def values(cls) -> Set[str]:
        """Returns the set of all member values."""
        return {member.value for _, member in cls.__members__.items()}

    def _generate_next_value_(self, start, count, last_values) -> str:
        del start, count, last_values
        return self.lower()


class Timeframe(AutoName):
    """Enumeration of the values for the timeframe option."""

    AFTERNOON = enum.auto()
    DAY = enum.auto()
    MORNING = enum.auto()
    NIGHT = enum.auto()


class Blockchain(AutoName):
    """Enumeration of the values for the blockcahin, white- or blacklist options."""

    BITCOIN = enum.auto()
    EOS = enum.auto()
    ETHEREUM = enum.auto()
    HYPERLEDGER = enum.auto()
    IOTA = enum.auto()
    MULTICHAIN = enum.auto()
    STELLAR = enum.auto()


class Profile(AutoName):
    """Enumeration of the values for the profile options."""

    CHEAPEST = enum.auto()
    FASTEST = enum.auto()


class Filter(AutoName):
    """Enumeration of the values for the filter options."""

    CHEAP = enum.auto()
    FAST = enum.auto()
    POPULAR = enum.auto()
    PRIVATE = enum.auto()
    PUBLIC = enum.auto()
    STABLE = enum.auto()


class Modifier(AutoName):
    """Enumeration of the values for the modifier options."""

    ENCRYPTION = enum.auto()
    REDUNDANCY = enum.auto()
    SPLITTING = enum.auto()


class Interval(AutoName):
    """Enumeration of the values for the cost interval option."""

    DAILY = enum.auto()
    WEEKLY = enum.auto()
    MONTHLY = enum.auto()
    YEARLY = enum.auto()


class Currency(AutoName):
    """Enumeration of the values for the cost currency option."""

    CHF = enum.auto()
    EUR = enum.auto()
    USD = enum.auto()


@dataclasses.dataclass
class Intent:
    """Intent represents an abstract, high-level policy."""
    users: Set[str] = field(default_factory=set)
    timeframe: Optional[Timeframe] = None
    blockchain: Optional[Blockchain] = None
    profile: Optional[Profile] = None
    filters: Set[Filter] = field(default_factory=set)
    whitelist: Set[Blockchain] = field(default_factory=set)
    blacklist: Set[Blockchain] = field(default_factory=set)
    modifiers: Set[Modifier] = field(default_factory=set)
    interval: Optional[Interval] = None
    currency: Optional[Currency] = None
    threshold: float = 0.0

    @property
    def raw(self) -> str:
        """Returns the corresponding raw intent as a string."""
        raw_intent = ""
        if self.users:
            raw_intent += f"for {join(iter(self.users))} "
        if self.timeframe:
            raw_intent += f"in the {self.timeframe.value} "
        if self.blockchain:
            raw_intent += f"select {self.blockchain.value} "
        if self.profile:
            raw_intent += f"select the {self.profile.value} "
            if self.filters:
                raw_intent += f"{join_enum(iter(self.filters))} "
            raw_intent += f"blockchain "
        if self.whitelist:
            raw_intent += f"from {join_enum(iter(self.whitelist))} "
        if self.blacklist:
            raw_intent += f"except {join_enum(iter(self.blacklist))} "
        if self.modifiers:
            raw_intent += f"with {join_enum(iter(self.modifiers))} "
        if self.interval and self.threshold:
            raw_intent += f"until the {self.interval.value} costs reach "
            if self.currency:
                raw_intent += f"{self.currency.value.upper()} "
            raw_intent += f"{self.threshold} "
        if not self.interval:
            raw_intent += f"as default"
        return raw_intent


def join_enum(members: Iterable[enum.Enum]) -> str:
    """Joins the values of the enum members and returns a string."""
    return join(member.value for member in members)


def join(values: Iterable[str]) -> str:
    """Joins the values returns a string.

    If a single value is passedh, this value is simply returned.
    If exactly two values are passed, these values are joined with 'and' surrounded by whitespace.
    If more than two values are passed, the last values are joined with 'and' surrounded by
    whitespace and the remaining values are joined with a comma and whitespace.
    """
    *other, last = values
    return f"{', '.join(other)} and {last}" if other else last
