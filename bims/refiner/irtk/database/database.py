import contextlib
from datetime import datetime

import sqlalchemy.orm
import sqlalchemy.ext.declarative
from sqlalchemy import \
    Boolean, \
    Column, \
    DateTime, \
    Enum, \
    func, \
    Float, \
    Integer, \
    PickleType, \
    String, \
    Table

from ..config import DATABASE_URI
from ..intent import Currency as IntentCurrency
from ..policy import BlockchainType, CostProfile, Currency as PolicyCurrency, Interval, Time, Policy


class Database:
    """Database connects to a database located at the given URI."""

    def __init__(self, database_uri: str = DATABASE_URI, init: bool = False) -> None:
        self._engine = sqlalchemy.create_engine(database_uri)
        self._session = sqlalchemy.orm.sessionmaker(bind=self._engine)
        if init:
            BASE.metadata.create_all(self._engine)

    @contextlib.contextmanager
    def session_scope(self) -> None:
        """Provide a transactional scope around a series of operations."""
        session = self._session()
        try:
            yield session
            session.commit()
        except BaseException:
            session.rollback()
            raise
        finally:
            session.close()


class Base:
    """Base database entity with some metadata.

    The metadata consists of an auto generated id, created_at and updated_at timestamps. The
    created_at timestamp corresponds to the creation of the database entity. Whenever the database
    entity is modified, the updated_at timestamp is updated.
    """

    @sqlalchemy.ext.declarative.declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)
    created_at: datetime = Column(DateTime, default=func.now())
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now())


BASE = sqlalchemy.ext.declarative.declarative_base(cls=Base)

# Sqlalchemy already defines a type called time, to resolve this name
# collision, we simply add an underscore as suffix to the name.
TIME = Enum(Time, name="time_")

# Here, we use the classical mapping of sqlalchemy, because the
# declarative mapping does not work well with Python dataclasses.
POLICY = Table(
    "policy",
    BASE.metadata,

    # Because we use the classical mapping and not the declarative mapping to
    # declare this table, we have to redefine the metadata columns below.
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),

    Column("user", String, nullable=False),
    Column("cost_profile", Enum(CostProfile), nullable=False),
    Column("timeframe_start", TIME, nullable=False),
    Column("timeframe_end", TIME, nullable=False),

    # Sqlalchemy already defines a type called interval, to resolve this name
    # collision, we simply add an underscore as suffix to the name.
    Column("interval", Enum(Interval, name="interval_"), nullable=False),

    # Both the policy and intent modules define their own Currency Enum type.
    # Because both are named Currency, we resolve this name collision by
    # explicitly adding a prefix to the name of the database type.
    Column("currency", Enum(PolicyCurrency, name="policy_currency"), nullable=False),

    Column("threshold", Float, nullable=False),
    Column("split_txs", Boolean, nullable=False),

    # We map this attribute (which is a Python set type) as a PickleType to
    # serialize it into a binary format. When updating this value, it has to
    # be reassigned for sqlalchemy to register the change.
    Column("blockchain_pool", PickleType, nullable=False),

    Column("blockchain_type", Enum(BlockchainType), nullable=False),
    Column("min_tx_rate", Integer, nullable=False),
    Column("max_block_time", Integer, nullable=False),
    Column("min_data_size", Integer, nullable=False),
    Column("max_tx_cost", Float, nullable=False),
    Column("min_popularity", Float, nullable=False),
    Column("min_stability", Float, nullable=False),
    Column("turing_complete", Boolean, nullable=False),
    Column("encryption", Boolean, nullable=False),
    Column("redundancy", Boolean, nullable=False),
)

sqlalchemy.orm.mapper(Policy, POLICY)


class Conversion(BASE):
    """Conversion Entity.

    Stores the conversion rate to convert currencies into us dollar.
    """

    # Both the policy and intent modules define their own Currency Enum type.
    # Because both are named Currency, we resolve this name collision by
    # explicitly adding a prefix to the name of the database type.
    currency: IntentCurrency = Column(
        Enum(IntentCurrency, name="intent_currency"),
        nullable=False,
        unique=True,
    )

    rate: float = Column(Float, nullable=False)
