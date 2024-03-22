"""Test"""

import unittest
from unittest.mock import Mock

from nmbrs.data_classes.company import Company
from nmbrs.data_classes.debtor import Debtor

from src.nmbrs_database import NmbrsDatabase
from src.nmbrs_database.db import BasicDatabase


class TestNmbrsDatabase(unittest.TestCase):
    """Test"""

    def setUp(self):
        """Test setup"""
        # Mocking Nmbrs API
        self.mock_api = Mock()
        self.db_url = "sqlite:///test_nmbrs.db"

        # Creating NmbrsDatabase instance
        self.nmbrs_db = NmbrsDatabase(self.mock_api, self.db_url)

        # Sample debtors
        self.sample_debtors = [Debtor({"Id": 1, "Name": "Debtor 1"}), Debtor({"Id": 2, "Name": "Debtor 2"})]
        self.sample_companies = [Company({"ID": 1, "Name": "Debtor 1"}), Company({"ID": 2, "Name": "Debtor 2"})]

    def test_create_basic_with_debtors(self):
        """test"""
        # Mocking debtor get_all method
        self.mock_api.debtor.get_all.return_value = self.sample_debtors
        self.mock_api.company.get_by_debtor.return_value = self.sample_companies

        # Calling create_basic method
        self.nmbrs_db.create_basic()

        # Asserting that the BasicDatabase was created with correct debtors
        self.assertIsInstance(self.nmbrs_db.database, BasicDatabase)
        self.mock_api.debtor.get_all.assert_called_once()
        self.mock_api.company.get_by_debtor.assert_called_once_with(debtor_id=1)
        self.mock_api.company.get_by_debtor.assert_called_once_with(debtor_id=2)
