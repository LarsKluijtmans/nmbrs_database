"""Abstract base class for databases."""

from abc import ABC, abstractmethod

import sqlalchemy
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
        delete: bool = False,
    ):
        """
        Initializes the Database.

        Args:
            api (Nmbrs): Nmbrs API instance used to interact with nmbrs.
            db_url (str): Database URL.
            base (declarative_base): Base class used to create the database.
            delete (bool, optional): Delete existing database.
        """
        self.api = api
        self.db_url = db_url
        self.base = base

        self.create_database()

        self.engine = create_engine(db_url)

        if delete:
            # Drop existing tables if they exist
            base.metadata.drop_all(self.engine)

        # Create tables based on metabase
        base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self):
        # Determine the database dialect from the URL
        db_dialect = sqlalchemy.engine.url.make_url(self.db_url).get_dialect().name

        # Check if the database exists, if not create it
        if db_dialect == 'mysql':
            self.create_mysql_database()
        elif db_dialect == 'postgresql':
            self.create_postgresql_database()

    def create_mysql_database(self):
        import mysql.connector  # pip install mysql-connector-python

        # Extract database name from db_url
        url = sqlalchemy.engine.url.make_url(self.db_url)
        connection = mysql.connector.connect(
            host=url.host,
            user=url.username,
            password=url.password,
            port=url.port,
        )

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()

        # Execute SQL command to create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(url.database))

        # Close the cursor and connection
        cursor.close()
        connection.close()

    def create_postgresql_database(self):
        # Extract database name from db_url
        url = sqlalchemy.engine.url.make_url(self.db_url)

        # Connect to server
        conn = self.engine.connect()

        # Execute SQL query to create the database if it doesn't exist
        conn.execute("CREATE DATABASE IF NOT EXISTS {}".format(url.database))
        conn.close()

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
