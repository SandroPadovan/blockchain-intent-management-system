from rest_framework.test import APITestCase
from rest_framework import status

from refiner.models import Currency
from intent_manager.models import Intent


class IntegrationTests(APITestCase):

    def setUp(self) -> None:
        # save currencies to database
        usd = Currency(currency='USD', exchange_rate=1)
        chf = Currency(currency='CHF', exchange_rate=1.09)
        eur = Currency(currency='EUR', exchange_rate=1.18)
        usd.save()
        chf.save()
        eur.save()

    def test_integration_test(self):
        # register a user and log in
        credentials = {'username': 'testUser0',
                       'password': 'password123'}

        registration_response = self.client.post('/api/auth/register', credentials, format='json')
        self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)

        token = registration_response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create two intents
        intent1 = 'For client1 select the fastest Blockchain as default'
        intent2 = 'For client2 select the cheapest Blockchain except EOS with redundancy and splitting until the ' \
                  'daily costs reach CHF 20'

        POST_intent1 = self.client.post('/api/intents/', {'intent_string': intent1}, format='json')
        self.assertEqual(POST_intent1.status_code, status.HTTP_201_CREATED,
                         'Incorrect status of POST request of intent1')
        self.assertEqual(Intent.objects.get(id=POST_intent1.data.get('id')).intent_string, intent1,
                         'Intent_string incorrect of intent1')

        POST_intent2 = self.client.post('/api/intents/', {'intent_string': intent2}, format='json')
        self.assertEqual(POST_intent2.status_code, status.HTTP_201_CREATED,
                         'Incorrect status of POST request of intent2')
        self.assertEqual(Intent.objects.get(id=POST_intent2.data.get('id')).intent_string, intent2,
                         'Intent_string incorrect of intent2')

        # get intents
        GET_intents = self.client.get('/api/intents/')
        self.assertEqual(GET_intents.status_code, status.HTTP_200_OK, 'Incorrect status of GET intents request')
        self.assertEqual(len(GET_intents.data), 2, 'Incorrect number of intents returned by GET intents request')

        intent_id1 = GET_intents.data[0]['id']
        intent_id2 = GET_intents.data[1]['id']

        # get policies of intent
        GET_policy1 = self.client.get('/api/policies/?intent_id=' + str(intent_id1))
        self.assertEqual(GET_policy1.status_code, status.HTTP_200_OK, 'Incorrect status of GET policies 1 request')
        self.assertEqual(len(GET_policy1.data), 1, 'Incorrect number of policies returned for intent1')

        GET_policy2 = self.client.get('/api/policies/?intent_id=' + str(intent_id2))
        self.assertEqual(GET_policy2.status_code, status.HTTP_200_OK, 'Incorrect status of GET policies 2 request')
        self.assertEqual(len(GET_policy2.data), 1, 'Incorrect number of policies returned for intent2')
        self.assertTrue('EOS' not in GET_policy2.data[0]['blockchain_pool'], 'EOS was in blockchain pool.')

        # update intent
        new_intent2 = 'For client2 and client3 select the cheapest Blockchain except Bitcoin with redundancy and ' \
                      'splitting until the daily costs reach 21'
        PUT_intent2 = self.client.put('/api/intents/' + str(intent_id2) + '/', {'intent_string': new_intent2}, format='json')
        self.assertEqual(PUT_intent2.status_code, status.HTTP_200_OK, 'Incorrect status of PUT intent')
        self.assertEqual(Intent.objects.get(id=intent_id2).intent_string, new_intent2)

        # get updated policies
        GET_updated_policy = self.client.get('/api/policies/?intent_id=' + str(intent_id2))
        self.assertEqual(GET_updated_policy.status_code, status.HTTP_200_OK, 'Incorrect status of GET policies2 request')
        self.assertEqual(len(GET_updated_policy.data), 2, 'Incorrect number of policies returned for intent2')
        self.assertEqual(GET_updated_policy.data[0]['threshold'], 21, 'Incorrect threshold of updated policy')
        self.assertTrue(GET_updated_policy.data[0]['threshold'] == GET_updated_policy.data[1]['threshold'],
                        'Thresholds of policies are not equal')
        self.assertTrue(bool(GET_updated_policy.data[0]['created_at'] != GET_updated_policy.data[0]['updated_at'])
                        != bool(GET_updated_policy.data[1]['created_at'] != GET_updated_policy.data[1]['updated_at']))
        self.assertTrue('BITCOIN' not in GET_updated_policy.data[0]['blockchain_pool'], 'BITCOIN was in blockchain pool.')
        self.assertTrue('EOS' in GET_updated_policy.data[0]['blockchain_pool'], 'EOS was not in blockchain pool.')

        DEL_intent = self.client.delete('/api/intents/' + str(intent_id2) + '/')
        self.assertEqual(DEL_intent.status_code, status.HTTP_204_NO_CONTENT, 'Intent was not deleted.')
        self.assertEqual(self.client.get('/api/intents/' + str(intent_id2) + '/').status_code, status.HTTP_404_NOT_FOUND)

        # log out
        POST_logout = self.client.post('/api/auth/logout/', None, format='json')
        self.assertEqual(POST_logout.status_code, status.HTTP_204_NO_CONTENT, 'Incorrect status of POST logout request')

        # test if logged out
        GET_intents_unauthorized = self.client.get('/api/intents/')
        self.assertEqual(GET_intents_unauthorized.status_code, status.HTTP_401_UNAUTHORIZED,
                         'Incorrect status of GET intents request')
