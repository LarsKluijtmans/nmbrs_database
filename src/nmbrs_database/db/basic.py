"""Insertion class for the nmbrs Basic database"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from nmbrs.data_classes.company import Company
from nmbrs.data_classes.debtor import Debtor
from nmbrs import Nmbrs
from sqlalchemy.orm import Session

from .database import Database
from ..models import BasicBase
from ..models.basic_model import DebtorDB, CompanyDB, EmployeeTypesDB, EmployeeDB
from ..utils.session_scope import session_scope


class BasicDatabase(Database):
    """Handles the insertion of data into the nmbrs Basic database."""

    def __init__(
        self,
        api: Nmbrs,
        db_url: str = "sqlite:///nmbrs.db",
    ):
        """
        Initializes the BasicDatabase.

        Args:
            api (Nmbrs): Nmbrs API used to request info from nmbrs.
            db_url (str, optional): URL to connect to the database.
        """
        super().__init__(api, db_url, BasicBase)

        self.employee_types = [1, 2, 3, 4, 5, 6, 7]

    def create(self, debtors: list[Debtor] = None) -> None:
        """
        Create a basic database containing all the debtors, companies and employees.

        Args:
            debtors (list[Debtor]): List of debtors to include in the database.
        """
        if not debtors:
            return

        # Get all data that only needs to be inserted once
        with session_scope(self.Session) as session:
            # Insert employee types into database
            employee_types = self.api.employee.get_types()
            employee_types_db = [EmployeeTypesDB(**employee_type.to_dict()) for employee_type in employee_types]
            session.add_all(employee_types_db)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._process_debtor, debtor) for debtor in debtors]
            for future in as_completed(futures):
                future.result()

    def _process_debtor(self, debtor: Debtor):
        """
        Process a debtor and its associated companies.

        Args:
            debtor (Debtor): The debtor to process.
        """
        with session_scope(self.Session) as session:
            # Insert debtor into database
            debtors_db = DebtorDB(**debtor.to_dict())
            session.add(debtors_db)
            session.commit()

            # Process companies associated with debtor
            companies = self.api.company.get_by_debtor(debtor.id)
            for company in companies:
                self._process_company(debtor, company, session)

    def _process_company(self, debtor: Debtor, company: Company, session: Session):
        """
        Process a company associated with a debtor and insert it into the database.


        Args:
            debtor (Debtor): The debtor associated with the company.
            company (Company): The company to process.
            session (Session): SQLAlchemy session object.
        """
        company_db = CompanyDB(**company.to_dict(), debtor_id=debtor.id)
        session.add(company_db)
        session.commit()

        for employee_type in self.employee_types:
            employees = self.api.employee.get_by_company(company.id, employee_type)
            employees_db = [EmployeeDB(**employee.to_dict(), company_id=company.id, type_id=employee_type) for employee in employees]
            session.add_all(employees_db)
            session.commit()
