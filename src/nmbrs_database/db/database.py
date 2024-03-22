"""Abstract base class for databases."""

from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from nmbrs import Nmbrs
from nmbrs.data_classes.debtor import Debtor


class Database(ABC):
    """Abstract base class for databases."""

    def __init__(
        self,
        api: Nmbrs,
        db_url: str,
        base: declarative_base,
    ):
        """
        Initializes the Database.

        Args:
            api (Nmbrs): Nmbrs API instance used to interact with nmbrs.
            db_url (str): Database URL.
            base (declarative_base): Base class used to create the database.
        """
        self.api = api
        self.engine = create_engine(db_url)
        self.base = base

        # Create tables based on metabase
        base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @abstractmethod
    def create(self, debtors: list[Debtor] = None) -> None:
        """
        Abstract method to create records in the database.

        Args:
            debtors (list[Debtor]): List of Debtor objects to create records for.
        """

    def query(self, query: str) -> any:
        """
        Execute a raw SQL query on the database.

        Args:
            query (str): SQL query to execute.

        Returns:
            any: Result of the query.
        """
        with self.engine.connect() as connection:
            compiled_query = text(query)
            result = connection.execute(compiled_query)
            return result.fetchall()

    def initialize(self) -> None:
        """
        Method to initialize the database connection.
        """
        try:
            # Try to connect to the database
            with self.engine.connect():
                print("Database connected successfully!")
        except OperationalError:
            print("Database does not exist or could not be connected to.")
