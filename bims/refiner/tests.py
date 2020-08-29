from django.test import TestCase
from .refiner import refine_intent, save_policies
from .models import Currency
from intent_manager.models import Intent
from user_manager.models import User
from policy_manager.models import Policy
from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, Time


class RefinerTests(TestCase):

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

    def test_save_single_policy(self):

        # save all necessary models
        user = User(username='testUser0')
        user.save()
        intent = Intent(username=user, intent_string='For client1 select the fastest Blockchain until the daily costs '
                                                     'reach 24')
        intent.save()

        # create irtkPolicy object
        policy = irtkPolicy(user='client1',
                            cost_profile=CostProfile.PERFORMANCE,
                            timeframe_start=Time.DEFAULT,
                            timeframe_end=Time.DEFAULT,
                            interval=Interval.DAILY,
                            currency=irtkCurrency.USD,
                            threshold=24.0,
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
        policy_list = [policy]

        save_policies(policy_list, 1)

        self.assertEqual(Policy.objects.count(), 1, 'More than one policy was saved.')
        self.assertEqual(Policy.objects.get().threshold, 24, 'Threshold incorrect')
        self.assertIsNotNone(Policy.objects.get().id, 'Policy id was None')
