import dataclasses
import logging
import unittest
from typing import Mapping

import ddt

from irtk.translator import Translator
from irtk.database.database import Database
from irtk.intent import Currency, Intent, Profile
from irtk.policy import CostProfile, Interval, Policy
from irtk.database.repository import Conversion, Repository

logging.disable(logging.CRITICAL)

CHF_CONVERSION_RATE = 1.05
EUR_CONVERSION_RATE = 1.10


@dataclasses.dataclass
class Test:
    intent_options: Mapping
    policy_options: Mapping
    options: Mapping = dataclasses.field(default_factory=dict)


@ddt.ddt
class TestTranslator(unittest.TestCase):
    _translator = None

    @classmethod
    def setUp(cls) -> None:
        database = Database("sqlite://", init=True)
        repository = Repository(database)
        repository.save(Conversion(currency=Currency.CHF, rate=CHF_CONVERSION_RATE))
        repository.save(Conversion(currency=Currency.EUR, rate=EUR_CONVERSION_RATE))
        cls._translator = Translator(repository)

    @ddt.data(
        Test(
            intent_options=dict(users={"client"}, profile=Profile.FASTEST),
            policy_options=dict(cost_profile=CostProfile.PERFORMANCE, interval=Interval.DEFAULT),
        ),
        Test(
            intent_options=dict(users={"client1", "client2"}, profile=Profile.CHEAPEST),
            policy_options=dict(cost_profile=CostProfile.ECONOMIC, interval=Interval.DEFAULT),
        ),
        Test(
            intent_options=dict(
                users={"client"},
                profile=Profile.CHEAPEST,
                threshold=25.0,
                currency=Currency.EUR,
            ),
            policy_options=dict(
                cost_profile=CostProfile.ECONOMIC,
                threshold=25.0 * EUR_CONVERSION_RATE,
            ),
            options=dict(interval=Interval.WEEKLY),
        ),
        Test(
            intent_options=dict(
                users={"client1", "client2"},
                profile=Profile.FASTEST,
                threshold=30.0,
                currency=Currency.CHF,
            ),
            policy_options=dict(
                cost_profile=CostProfile.PERFORMANCE,
                threshold=30.0 * CHF_CONVERSION_RATE,
            ),
            options=dict(interval=Interval.DAILY),
        ),
    )
    def test_translate(self, test: Test):
        intent = Intent(**test.intent_options, **test.options)
        policies = self._translator.translate(intent)
        self.assertCountEqual(policies, [
            Policy(user=user, **test.policy_options, **test.options) for user in iter(intent.users)
        ])


if __name__ == "__main__":
    unittest.main()
