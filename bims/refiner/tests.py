from django.test import TestCase, override_settings
import time

from .refiner import refine_intent, save_policies, update_policies

from .models import Currency
from intent_manager.models import Intent
from user_manager.models import User
from policy_manager.models import Policy

from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, \
    Time


@override_settings(USE_PLEBEUS=False)
class RefinementTests(TestCase):

    def setUp(self) -> None:
        # save currencies to database
        usd = Currency(currency='USD', exchange_rate=1)
        chf = Currency(currency='CHF', exchange_rate=1.09)
        eur = Currency(currency='EUR', exchange_rate=1.18)
        usd.save()
        chf.save()
        eur.save()

    def test_refine_default_intent(self):
        intent = 'For client1 select the fastest Blockchain as default'

        policy = refine_intent(intent)

        self.assertEqual(len(policy), 1, 'More than 1 policy were created')
        self.assertEqual(policy[0].user, 'client1')
        self.assertEqual(policy[0].cost_profile, CostProfile.PERFORMANCE)

    def test_refine_CHF_intent(self):
        threshold = 20
        intent = 'For client1 select the cheapest Blockchain until the daily costs reach CHF ' + str(threshold)

        policy = refine_intent(intent)
        exchange_rate = Currency.objects.get(currency='CHF').exchange_rate

        self.assertEqual(len(policy), 1, 'More than 1 policy were created')
        self.assertEqual(policy[0].threshold, threshold * exchange_rate)

    def test_refine_multiple_user_intent(self):
        intent = 'For client1, client2 and client3 select the cheapest Blockchain as default'

        policies = refine_intent(intent)

        self.assertEqual(len(policies), 3, 'Not 3 policy were created')


@override_settings(USE_PLEBEUS=False)
class RefinerPolicyManipulationTests(TestCase):
    intent = None

    def setUp(self) -> None:
        # save currencies to database
        usd = Currency(currency='USD', exchange_rate=1)
        chf = Currency(currency='CHF', exchange_rate=1.09)
        eur = Currency(currency='EUR', exchange_rate=1.18)
        usd.save()
        chf.save()
        eur.save()

        user = User(username='testUser0')
        user.save()
        self.intent = Intent(username=user,
                             intent_string='For client1 select the fastest Blockchain until the daily costs '
                                           'reach 24')
        self.intent.save()

    def test_save_single_policy(self):
        irtk_policy = irtk_policy_factory('client1', 24)
        policy_list = [irtk_policy]

        save_policies(policy_list, self.intent.id)

        self.assertEqual(Policy.objects.count(), 1, 'More than one policy was saved.')
        self.assertEqual(Policy.objects.get().threshold, 24, 'Threshold incorrect')
        self.assertIsNotNone(Policy.objects.get().id, 'Policy id was None')

    def test_update_single_policy(self):
        policy = Policy(intent_id=self.intent, currency=Currency.objects.get(currency='USD'))
        policy.save()

        irtk_policy = irtk_policy_factory('client2', 10)
        policy_list = [irtk_policy]

        update_policies(policy_list, self.intent.id)

        self.assertEqual(len(Policy.objects.all()), 1, 'Incorrect number of policies in database')
        self.assertEqual(Policy.objects.get().threshold, 10, 'Incorrect threshold of policy')
        self.assertEqual(Policy.objects.get().user, 'client2', 'Incorrect policy user')

    def test_update_policies_with_deleting_policies(self):
        policy1 = Policy(intent_id=self.intent, currency=Currency.objects.get(currency='USD'))
        policy1.save()
        policy2 = Policy(intent_id=self.intent, currency=Currency.objects.get(currency='USD'))
        policy2.save()

        irtk_policy = irtk_policy_factory('client3', 22)
        policy_list = [irtk_policy]

        update_policies(policy_list, self.intent.id)

        self.assertEqual(len(Policy.objects.all()), 1, 'Incorrect number of policies in database')
        self.assertEqual(Policy.objects.get().threshold, 22, 'Incorrect threshold of policy')
        self.assertEqual(Policy.objects.get().user, 'client3', 'Incorrect policy user')

    def test_update_policies_with_adding_policies(self):
        policy = Policy(intent_id=self.intent, currency=Currency.objects.get(currency='USD'))
        policy.save()

        irtk_policy1 = irtk_policy_factory('client1', 19)
        irtk_policy2 = irtk_policy_factory('client2', 12)
        policy_list = [irtk_policy1, irtk_policy2]

        time.sleep(0.01)    # test was flaky when comparing timestamps

        update_policies(policy_list, self.intent.id)

        self.assertEqual(len(Policy.objects.all()), 2, 'Incorrect number of policies in database')
        self.assertEqual(Policy.objects.filter(user='client1')[0].threshold, 19, 'Incorrect threshold of policy')
        self.assertEqual(Policy.objects.filter(user='client2')[0].threshold, 12, 'Incorrect threshold of policy')
        self.assertTrue(bool(Policy.objects.all()[0].created_at != Policy.objects.all()[0].updated_at)
                        != bool(Policy.objects.all()[1].created_at != Policy.objects.all()[1].updated_at))


def irtk_policy_factory(user: str, threshold: int) -> irtkPolicy:
    """helper function which returns an instance of irtkPolicy which can be used in tests"""
    irtk_policy = irtkPolicy(
        user=user,
        cost_profile=CostProfile.PERFORMANCE,
        timeframe_start=Time.DEFAULT,
        timeframe_end=Time.DEFAULT,
        interval=Interval.DAILY,
        currency=irtkCurrency.USD,
        threshold=threshold,
        split_txs=False,
        blockchain_pool=set(),
        blockchain_type=BlockchainType.INDIFFERENT,
        min_tx_rate=4,
        max_block_time=600,
        min_data_size=20,
        max_tx_cost=0.0,
        min_popularity=0.0,
        min_stability=0.0,
        turing_complete=False,
        encryption=False,
        redundancy=False
    )
    return irtk_policy
