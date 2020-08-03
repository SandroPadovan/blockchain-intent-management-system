import logging
import unittest
from typing import Type

import ddt

from irtk.intent import Blockchain, Currency, Filter, Intent, Interval, Modifier, Profile, Timeframe
from irtk.parser.state import \
    BlacklistState, \
    BlacklistWithUntilAsState, \
    BlockchainState, \
    CostsState, \
    CurrencyThresholdState, \
    DefaultState, \
    DefaultPolicyState, \
    ErrorState, \
    FilterBlockchainState, \
    FilterState, \
    FilterStateValidator, \
    ForState, \
    FromExceptWithUntilAsState, \
    IllegalTransitionError, \
    InSelectState, \
    IntervalState, \
    ModifierState, \
    PolicyState, \
    ProfileState, \
    ReachState, \
    SelectState, \
    The2State, \
    TheBlockchainState, \
    TheState, \
    ThresholdState, \
    TimeframeState, \
    UntilAsState, \
    UserState, \
    WhitelistState, \
    WhitelistWithUntilAsState, \
    WithUntilAsState
from irtk.validation import ValidationError

logging.disable(logging.CRITICAL)


@ddt.ddt
class TestForState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ForState()
        self._intent = Intent()

    @ddt.data(("for", UserState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestUserState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = UserState()
        self._intent = Intent()

    @ddt.data("client")
    def test_run(self, user: str) -> None:
        self.assertIsInstance(self._state.run(user, self._intent), InSelectState)

    @ddt.data("client")
    def test_validate(self, user: str) -> None:
        self._state._validate(user, self._intent)
        self.assertIn(user, self._intent.users)


@ddt.ddt
class TestInSelectState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = InSelectState(UserState())
        self._intent = Intent()

    @ddt.data(
        *((token, UserState) for token in {"and", ","}),
        ("in", TheState), ("select", TheBlockchainState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestTheState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = TheState()
        self._intent = Intent()

    @ddt.data(("the", TimeframeState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestTimeframeState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = TimeframeState()
        self._intent = Intent()

    @ddt.data(*((timeframe.value, SelectState) for timeframe in Timeframe))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Timeframe)
    def test_validate(self, timeframe: Timeframe) -> None:
        self._state._validate(timeframe.value, self._intent)
        self.assertEqual(self._intent.timeframe, timeframe)


@ddt.ddt
class TestSelectState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = SelectState()
        self._intent = Intent()

    @ddt.data(("select", TheBlockchainState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestTheBlockchainState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = TheBlockchainState()
        self._intent = Intent()

    @ddt.data(
        *((blockchain.value, WithUntilAsState) for blockchain in Blockchain),
        ("the", ProfileState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Blockchain)
    def test_validate_success(self, blockchain: Blockchain) -> None:
        self._state._validate(blockchain.value, self._intent)
        self.assertEqual(self._intent.blockchain, blockchain)

    def test_validate_error(self) -> None:
        self._state._validate("invalid", self._intent)
        self.assertIsNone(self._intent.blockchain)


@ddt.ddt
class TestWithUntilUseState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = WithUntilAsState()
        self._intent = Intent()

    @ddt.data(("with", ModifierState), ("until", The2State), ("as", DefaultState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestProfileState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ProfileState()
        self._intent = Intent()

    @ddt.data(*((profile.value, FilterBlockchainState) for profile in Profile))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Profile)
    def test_validate(self, profile: Profile) -> None:
        self._state._validate(profile.value, self._intent)
        self.assertEqual(self._intent.profile, profile)


@ddt.ddt
class TestFilterStateValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._validator = FilterStateValidator()
        self._intent = Intent()

    @ddt.data(*Filter)
    def test_validate_success(self, filter_: Filter) -> None:
        self._validator.validate(filter_.value, self._intent)
        self.assertIn(filter_, self._intent.filters)

    def test_validate_error(self) -> None:
        self._validator.validate("invalid", self._intent)
        self.assertSetEqual(self._intent.filters, set())

    def test_validate_private_public(self) -> None:
        self._intent.filters.add(Filter.PRIVATE)
        self.assertRaises(
            ValidationError,
            self._validator.validate,
            Filter.PUBLIC.value,
            self._intent,
        )

    @ddt.data((Profile.CHEAPEST, Filter.CHEAP), (Profile.FASTEST, Filter.FAST))
    @ddt.unpack
    def test_validate_profile_filter(self, profile: Profile, filter_: Filter) -> None:
        self._intent.profile = profile
        self._validator.validate(filter_.value, self._intent)
        self.assertNotIn(filter_, self._intent.filters)


@ddt.ddt
class TestFilterBlockchainState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = FilterBlockchainState()
        self._intent = Intent()

    @ddt.data(
        *((filter_.value, BlockchainState) for filter_ in Filter),
        ("blockchain", FromExceptWithUntilAsState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestFilterState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = FilterState()
        self._intent = Intent()

    @ddt.data(*((filter_.value, BlockchainState) for filter_ in Filter))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestBlockchainState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = BlockchainState(FilterState())
        self._intent = Intent()

    @ddt.data(
        *((token, FilterState) for token in {"and", ","}),
        ("blockchain", FromExceptWithUntilAsState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestFromExceptWithUntilUseState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = FromExceptWithUntilAsState()
        self._intent = Intent()

    @ddt.data(
        ("from", WhitelistState),
        ("except", BlacklistState),
        ("with", ModifierState),
        ("until", The2State),
        ("as", DefaultState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestWhitelistState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = WhitelistState()
        self._intent = Intent()

    @ddt.data(*((blockchain.value, WhitelistWithUntilAsState) for blockchain in Blockchain))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Blockchain)
    def test_validate(self, blockchain: Blockchain) -> None:
        self._state._validate(blockchain.value, self._intent)
        self.assertIn(blockchain, self._intent.whitelist)


@ddt.ddt
class TestWhitelistWithUntilUseState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = WhitelistWithUntilAsState(WhitelistState())
        self._intent = Intent()

    @ddt.data(
        *((token, WhitelistState) for token in {"and", ","}),
        ("with", ModifierState),
        ("until", The2State),
        ("as", DefaultState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestBlacklistState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = BlacklistState()
        self._intent = Intent()

    @ddt.data(*((blockchain.value, BlacklistWithUntilAsState) for blockchain in Blockchain))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Blockchain)
    def test_validate(self, blockchain: Blockchain) -> None:
        self._state._validate(blockchain.value, self._intent)
        self.assertIn(blockchain, self._intent.blacklist)


@ddt.ddt
class TestBlacklistWithUntilAsState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = BlacklistWithUntilAsState(BlacklistState())
        self._intent = Intent()

    @ddt.data(
        *((token, BlacklistState) for token in {"and", ","}),
        ("with", ModifierState),
        ("until", The2State),
        ("as", DefaultState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestModifierState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ModifierState()
        self._intent = Intent()

    @ddt.data(*((modifier.value, UntilAsState) for modifier in Modifier))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Modifier)
    def test_validate(self, modifier: Modifier) -> None:
        self._state._validate(modifier.value, self._intent)
        self.assertIn(modifier, self._intent.modifiers)


@ddt.ddt
class TestUntilAsState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = UntilAsState(ModifierState())
        self._intent = Intent()

    @ddt.data(
        *((token, ModifierState) for token in {"and", ","}),
        ("until", The2State),
        ("as", DefaultState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestThe2State(unittest.TestCase):
    def setUp(self) -> None:
        self._state = The2State()
        self._intent = Intent()

    @ddt.data(("the", IntervalState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestIntervalState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = IntervalState()
        self._intent = Intent()

    @ddt.data(*((interval.value, CostsState) for interval in Interval))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Interval)
    def test_validate(self, interval: Interval) -> None:
        self._state._validate(interval.value, self._intent)
        self.assertEqual(self._intent.interval, interval)


@ddt.ddt
class TestCostsState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = CostsState()
        self._intent = Intent()

    @ddt.data(("costs", ReachState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestReachState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ReachState()
        self._intent = Intent()

    @ddt.data(("reach", CurrencyThresholdState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)


@ddt.ddt
class TestCurrencyThresholdState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = CurrencyThresholdState()
        self._intent = Intent()

    @ddt.data(
        *((currency.value, ThresholdState) for currency in Currency),
        ("47.2", PolicyState),
    )
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", ValidationError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Currency)
    def test_validate(self, currency: Currency) -> None:
        self._state._validate(currency.value, self._intent)
        self.assertEqual(self._intent.currency, currency)


@ddt.ddt
class TestThresholdState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ThresholdState()
        self._intent = Intent()

    @ddt.data(("35.7", PolicyState))
    @ddt.unpack
    def test_run(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", ValidationError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(15.7)
    def test_validate(self, threshold: float) -> None:
        self._state._validate(str(threshold), self._intent)
        self.assertEqual(self._intent.threshold, threshold)

    def test_validate_error(self) -> None:
        self.assertRaises(ValidationError, self._state._validate, "invalid", self._intent)


@ddt.ddt
class TestPolicyState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = PolicyState()
        self._intent = Intent()

    @ddt.data("random")
    def test_run(self, token: str) -> None:
        self.assertRaises(IllegalTransitionError, self._state.run, token, self._intent)


@ddt.ddt
class TestDefaultState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = DefaultState()
        self._intent = Intent()

    @ddt.data(("default", DefaultPolicyState))
    @ddt.unpack
    def test_run_success(self, token: str, successor_state: type) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), successor_state)

    @ddt.data(("invalid", IllegalTransitionError))
    @ddt.unpack
    def test_run_error(self, token: str, exception: Type[Exception]) -> None:
        self.assertRaises(exception, self._state.run, token, self._intent)

    @ddt.data(*Timeframe)
    def test_validate(self, timeframe: Timeframe) -> None:
        self._intent.timeframe = timeframe
        self._state._validate("default", self._intent)
        self.assertIsNone(self._intent.timeframe)
        self.assertIsNone(self._intent.interval)


@ddt.ddt
class TestDefaultPolicyState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = DefaultPolicyState()
        self._intent = Intent()

    @ddt.data("random")
    def test_run(self, token: str) -> None:
        self.assertRaises(IllegalTransitionError, self._state.run, token, self._intent)


@ddt.ddt
class TestErrorState(unittest.TestCase):
    def setUp(self) -> None:
        self._state = ErrorState()
        self._intent = Intent()

    @ddt.data("random")
    def test_run(self, token: str) -> None:
        self.assertIsInstance(self._state.run(token, self._intent), ErrorState)


if __name__ == "__main__":
    unittest.main()
