from django.test import TestCase
from .refiner import refine_intent
from .models import Currency


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
