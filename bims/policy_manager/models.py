from django.db import models
from intent_manager.models import Intent
from refiner.models import Currency
from .policy_manager import PolicyManager


class Policy(models.Model):
    intent_id = models.ForeignKey(Intent, on_delete=models.CASCADE)
    pbs_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=100)
    cost_profile = models.CharField(max_length=100)
    timeframe_start = models.CharField(max_length=100, default='00.00')
    timeframe_end = models.CharField(max_length=100, default='00.00')
    interval = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    threshold = models.FloatField(default=0)
    split_txs = models.BooleanField(default=False)

    # blockchain_pool is pickled and stored as a binary string.
    # To unpickle: pickle.loads(blockchain_pool)
    blockchain_pool = models.BinaryField(max_length=300)
    blockchain_type = models.CharField(max_length=100)
    min_tx_rate = models.IntegerField(default=4)
    max_block_time = models.IntegerField(default=600)
    min_data_size = models.IntegerField(default=20)
    max_tx_cost = models.FloatField(default=0)
    min_popularity = models.FloatField(default=0)
    min_stability = models.FloatField(default=0)
    turing_complete = models.BooleanField(default=False)
    encryption = models.BooleanField(default=False)
    redundancy = models.BooleanField(default=False)

    objects = PolicyManager()
