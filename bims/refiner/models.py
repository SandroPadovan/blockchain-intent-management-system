from django.db import models


class Currency(models.Model):
    currency = models.CharField(primary_key=True, max_length=3)
    exchange_rate = models.FloatField(default=1)
