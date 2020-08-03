import dataclasses
from dataclasses import field
import enum
import json
from typing import Any, Dict, Set

from .config import TIME_DAY_START, TIME_AFTERNOON_START, TIME_NIGHT_START
from .intent import Blockchain


class Time(enum.Enum):
    """Enumeration of the time option."""

    DEFAULT = "00:00"
    DAY_START = TIME_DAY_START
    AFTERNOON_START = TIME_AFTERNOON_START
    NIGHT_START = TIME_NIGHT_START


class AutoName(enum.Enum):
    """Base enum that automatically sets the values based on the member name."""

    def _generate_next_value_(self, start, count, last_values) -> str:
        del start, count, last_values
        return self.lower()


class CostProfile(AutoName):
    """Enumeration of the cost profile option."""

    ECONOMIC = enum.auto()
    PERFORMANCE = enum.auto()


# Actually, the Policy-based Blockchain Selection Framework supports other
# currencies as well. Specifically, it also supports swiss francs (CHF)
# and euros (EUR). However, to support other currencies, we always set us
# dollar (USD) as currency and convert the threshold values, if needed.
# Therefore, we are able to independently support other currencies as
# well, without changing the Policy-based Blockchain Selection Framework.
class Currency(AutoName):
    """Enumeration of the cost currency option."""

    USD = enum.auto()


class Interval(AutoName):
    """Enumeration of the cost interval option."""

    DEFAULT = enum.auto()
    DAILY = enum.auto()
    WEEKLY = enum.auto()
    MONTHLY = enum.auto()
    YEARLY = enum.auto()


class BlockchainType(AutoName):
    """Enumeration of the blockchain type option."""

    INDIFFERENT = enum.auto()
    PRIVATE = enum.auto()
    PUBLIC = enum.auto()


@dataclasses.dataclass
class Policy:
    """Policy represents a low-level policy."""

    # Python dataclasses and sqlalchemy do not work well together. More
    # precisely, the default attribute of dataclasses.field is not mapped
    # properly by sqlalchemy. As a workaround, we use the default_factory
    # attribute of dataclasses.field which in fact is properly mapped by
    # sqlalchemy. More information:
    # https://stackoverflow.com/questions/55577165/sqlalchemy-with-dataclass-default-not-populating-postgres-database
    user: str = field(default_factory=str)
    cost_profile: CostProfile = field(default_factory=lambda: CostProfile.ECONOMIC)
    timeframe_start: Time = field(default_factory=lambda: Time.DEFAULT)
    timeframe_end: Time = field(default_factory=lambda: Time.DEFAULT)
    interval: Interval = field(default_factory=lambda: Interval.DEFAULT)
    currency: Currency = field(default_factory=lambda: Currency.USD)
    threshold: float = field(default_factory=float)
    split_txs: bool = field(default_factory=bool)
    blockchain_pool: Set[Blockchain] = field(default_factory=set)
    blockchain_type: BlockchainType = field(default_factory=lambda: BlockchainType.INDIFFERENT)

    # The default values for min_tx_rate, max_block_time, and min_data_size are taken from the
    # Policy-based Blockchain Selection Framework.
    min_tx_rate: int = field(default_factory=lambda: 4)
    max_block_time: int = field(default_factory=lambda: 600)
    min_data_size: int = field(default_factory=lambda: 20)

    # The cheap, popular, and stable filters are not supported by the Policy-based Blockchain
    # Selection Framework. The handling of these filters has to be implemented externally, e.g.,
    # by the Policy-based Blockchain Selection Framework.
    max_tx_cost: float = field(default_factory=float)
    min_popularity: float = field(default_factory=float)
    min_stability: float = field(default_factory=float)

    turing_complete: bool = field(default_factory=bool)

    # The encryption and redundancy modifiers are actually not supported by the Policy-based
    # Blockchain Selection Framework.
    encryption: bool = field(default_factory=bool)
    redundancy: bool = field(default_factory=bool)

    def asjson(self) -> str:
        """Returns a JSON representation of the specified policy options.

        Uses the format that the Policy-based Blockchain Selectin Framework expects.
        """
        return json.dumps(self.asdict())

    def asdict(self) -> Dict[str, Any]:
        """Returns a dict of the specified policy options.

        Uses the format that the Policy-based Blockchain Selectin Framework expects.
        """
        # We do not map all the attributes, because this adapts a policy for the
        # Policy-based Blockchain Selection Framework which does not support all
        # the attributes (e.g. encryption).
        return {
            "username": self.user,
            "costProfile": self.cost_profile.value,
            "timeFrameStart": self.timeframe_start.value,
            "timeFrameEnd": self.timeframe_end.value,
            "interval": self.interval.value,
            "currency": self.currency.value.upper(),
            "cost": self.threshold,
            "split": self.split_txs,
            "preferredBC": list(self.blockchain_pool),
            "bcType": self.blockchain_type.value,
            "bcTps": self.min_tx_rate,
            "bcBlockTime": self.max_block_time,
            "bcDataSize": self.min_data_size,
            "bcTuringComplete": self.turing_complete,
        }
