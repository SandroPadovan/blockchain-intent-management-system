from typing import Any, Optional

from .database import Conversion, Database
from ..intent import Currency


class Repository:
    """Repository acts as a data access layer."""

    def __init__(self, database: Optional[Database] = None) -> None:
        self._database = database or Database()

    def save(self, entity: Any) -> None:
        """Persists entity in the database."""
        with self._database.session_scope() as session:
            session.add(entity)

    def find_conversion_rate(self, currency: Currency) -> float:
        """Finds the conversion rate from the database for a currency."""
        with self._database.session_scope() as session:
            conversion = session.query(Conversion.rate).filter_by(currency=currency).one()
            return conversion.rate
