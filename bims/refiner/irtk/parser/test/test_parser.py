import logging
import unittest

import ddt

from irtk.intent import Blockchain, Currency, Filter, Intent, Interval, Modifier, Profile, Timeframe
from irtk.parser.parser import Parser
from irtk.parser.state import IllegalTransitionError
from irtk.validation import ValidationError

logging.disable(logging.CRITICAL)


@ddt.ddt
class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = Parser()

    @ddt.data(
        Intent(users={"client"}, profile=Profile.CHEAPEST),
        Intent(users={"client"}, blockchain=Blockchain.BITCOIN),
        *(
            Intent(
                users={"client"},
                profile=Profile.FASTEST,
                interval=Interval.DAILY,
                threshold=10.0,
                **options,
            ) for options in ({}, dict(currency=Currency.CHF))
        ),
        *(
            Intent(
                users={"client"},
                blockchain=Blockchain.ETHEREUM,
                interval=Interval.MONTHLY,
                threshold=35.0,
                **options,
            ) for options in ({}, dict(currency=Currency.EUR))
        ),
        *(
            Intent(
                users={"client"},
                timeframe=Timeframe.DAY,
                profile=Profile.CHEAPEST,
                filters={Filter.FAST, Filter.POPULAR, Filter.PUBLIC},
                whitelist={Blockchain.BITCOIN, Blockchain.ETHEREUM, Blockchain.MULTICHAIN},
                modifiers={Modifier.ENCRYPTION, Modifier.REDUNDANCY},
                interval=Interval.WEEKLY,
                threshold=20.0,
                **options,
            ) for options in ({}, dict(currency=Currency.USD))
        ),
        Intent(
            users={"client"},
            profile=Profile.FASTEST,
            filters={Filter.CHEAP, Filter.STABLE},
            whitelist={Blockchain.BITCOIN, Blockchain.MULTICHAIN},
            modifiers={Modifier.REDUNDANCY, Modifier.SPLITTING},

        ),
    )
    def test_parse_success(self, intent: Intent) -> None:
        parsed_intent = self._parser.parse(intent.raw)
        self.assertEqual(parsed_intent, intent)

    @ddt.data(
        Intent(users={"client"}),
        *(
            Intent(users={"client"}, interval=Interval.YEARLY, threshold=60.0, **options)
            for options in ({}, dict(currency=Currency.CHF))
        ),
        Intent(
            users={"client"},
            blockchain=Blockchain.MULTICHAIN,
            whitelist={Blockchain.BITCOIN},

        ),
        *(
            Intent(
                users={"client"},
                blockchain=Blockchain.ETHEREUM,
                whitelist={Blockchain.BITCOIN, Blockchain.MULTICHAIN},
                interval=Interval.DAILY,
                threshold=15.0,
                **options,
            ) for options in ({}, dict(currency=Currency.USD))
        ),
    )
    def test_parse_illegal_transition_error(self, intent: Intent) -> None:
        self.assertRaises(IllegalTransitionError, self._parser.parse, intent.raw)

    @ddt.data(
        *(
            Intent(
                users={"client"},
                profile=Profile.FASTEST,
                filters={Filter.PRIVATE, Filter.PUBLIC},
                interval=Interval.WEEKLY,
                threshold=30.0,
                **options,
            ) for options in ({}, dict(currency=Currency.CHF))
        ),
    )
    def test_parse_validaiton_error(self, intent: Intent) -> None:
        self.assertRaises(ValidationError, self._parser.parse, intent.raw)

    @ddt.data(
        *(
            (
                Intent(users={"client"}, interval=Interval.MONTHLY, threshold=25.0, **options),
                Profile.CHEAPEST,
                Filter.CHEAP,
            ) for options in ({}, dict(currency=Currency.EUR))
        ),
        *(
            (
                Intent(users={"client"}, interval=Interval.YEARLY, threshold=50.0, **options),
                Profile.FASTEST,
                Filter.FAST,
            ) for options in ({}, dict(currency=Currency.CHF))
        ),
    )
    @ddt.unpack
    def test_profile_filter(self, intent: Intent, profile: Profile, filter_: Filter) -> None:
        intent.profile = profile
        intent.filters.add(filter_)
        parsed_intent = self._parser.parse(intent.raw)
        self.assertNotIn(filter_, parsed_intent.filters)

    def test_parse_timeframe_default_policy(self) -> None:
        intent = Intent(
            users={"client"},
            timeframe=Timeframe.AFTERNOON,
            blockchain=Blockchain.MULTICHAIN,
        )
        parsed_intent = self._parser.parse(intent.raw)
        self.assertIsNone(parsed_intent.timeframe)


if __name__ == "__main__":
    unittest.main()
