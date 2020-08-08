from typing import Any, Optional

from .database import Database
from ..intent import Currency as CurrencyEnum
from refiner.models import Currency


class Repository:
    """Repository acts as a data access layer."""

    def __init__(self, database: Optional[Database] = None) -> None:
        self._database = database or Database()

    def save(self, entity: Any) -> None:
        """Persists entity in the database."""
        with self._database.session_scope() as session:
            session.add(entity)

    @staticmethod
    def find_conversion_rate(currency: CurrencyEnum) -> float:
        """Finds the conversion rate from the database for a currency."""

        # Accesses the django project database, not the irtk database
        exchange_rate = Currency.objects.get(currency=currency.name).exchange_rate
        return exchange_rate
