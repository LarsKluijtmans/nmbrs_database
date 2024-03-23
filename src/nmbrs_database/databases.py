"""Database class capable of creating databases with Nmbrs information."""

from nmbrs import Nmbrs
from nmbrs.data_classes.debtor import Debtor
from src.nmbrs_database.db import Database, BasicDatabase


class NmbrsDatabase:
    """Database class capable of creating databases with Nmbrs information."""

    def __init__(
        self,
        api: Nmbrs,
        db_url: str,
    ):
        """
        Initializes the NmbrsDatabase.

        Args:
            api (Nmbrs): Nmbrs API instance used to interact with Nmbrs.
            db_url (str): URL for the database.
        """
        self.api = api
        self.db_url = db_url
        self.database: Database | None = None

    def query(self, query: str) -> any:
        """
        Perform a query on the database.

        Args:
            query (str): Query to execute.

        Returns:
            any: Result of the query.
        """
        return self.database.query(query)

    def initialize_basic(self) -> None:
        """
        Initialize a basic database containing all the debtors, companies, and employees.
        """
        self.database = BasicDatabase(self.api, self.db_url)
        self.database.initialize()

    def create_basic(self, debtors: list[Debtor] = None, delete: bool = False) -> None:
        """
        Create a basic database containing all the debtors, companies, and employees.

        Args:
            debtors (list[Debtor], optional): List of debtors to include in the database. If None, all debtors are fetched.
            delete (bool, optional): Delete existing database.
        """
        if debtors is None:
            debtors = self.api.debtor.get_all()

        self.database = BasicDatabase(self.api, self.db_url, delete=delete)

        self.database.create(debtors)
