"""Base for the basic nmbrs database"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BasicBase = declarative_base()


class DebtorDB(BasicBase):
    """Debtor table"""

    __tablename__ = "debtors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)

    companies = relationship("CompanyDB", back_populates="debtor")


class CompanyDB(BasicBase):
    """Company table"""

    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    debtor_id = Column(Integer, ForeignKey("debtors.id"))
    number = Column(Integer)
    name = Column(String)
    phone_number = Column(String)
    fax_number = Column(String)
    email = Column(String)
    website = Column(String)
    loonaangifte_tijdvak = Column(String)
    kvk_number = Column(String)

    debtor = relationship("DebtorDB", back_populates="companies")
    employees = relationship("EmployeeDB", back_populates="company")


class EmployeeTypesDB(BasicBase):
    """Employee Types table"""

    __tablename__ = "employee_types"
    id = Column(Integer, primary_key=True)
    description = Column(String)

    employees = relationship("EmployeeDB", back_populates="type")


class EmployeeDB(BasicBase):
    """Employee table"""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    type_id = Column(Integer, ForeignKey("employee_types.id"))
    number = Column(Integer)
    name = Column(String)

    company = relationship("CompanyDB", back_populates="employees")
    type = relationship("EmployeeTypesDB", back_populates="employees")
