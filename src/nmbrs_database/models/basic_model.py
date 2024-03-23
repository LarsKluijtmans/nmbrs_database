"""Base for the basic nmbrs database"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BasicBase = declarative_base()


# Debtor level
debtors_tags_association = Table(
    'debtors_tags_association',
    BasicBase.metadata,
    Column('debtor_id', Integer, ForeignKey('debtors.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class DebtorDB(BasicBase):
    """Debtor table"""

    __tablename__ = "debtors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)

    companies = relationship("CompanyDB", back_populates="debtor")
    tags = relationship("TagDB", secondary=debtors_tags_association, backref="debtors")


class TagDB(BasicBase):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    hex_color = Column(String)
    tag = Column(String)

    __table_args__ = (
        UniqueConstraint('number', 'hex_color', 'tag', name='unique_number_hex_color_tag'),
    )


# Company level
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


# class Address(Base):
#     __tablename__ = 'address'
#
#     id = Column(Integer, primary_key=True)
#     default = Column(Boolean)
#     street = Column(String)
#     house_number = Column(String)
#     house_number_addition = Column(String)
#     postal_code = Column(String)
#     city = Column(String)
#     state_province = Column(String)
#     country_iso_code = Column(String)
#
# class BankAccount(Base):
#     __tablename__ = 'bank_account'
#
#     id = Column(Integer, primary_key=True)
#     number = Column(String)
#     description = Column(String)
#     iban = Column(String)
#     bic = Column(String)
#     city = Column(String)
#     name = Column(String)
#     type = Column(String)
#
# class ContactInfo(Base):
#     __tablename__ = 'contact_info'
#
#     id = Column(Integer, primary_key=True)
#     email = Column(String)
#     name = Column(String)
#     phone = Column(String)
#
# class Debtor(Base):
#     __tablename__ = 'debtor'
#
#     id = Column(Integer, primary_key=True)
#     number = Column(String)
#     name = Column(String)
#
# class Department(Base):
#     __tablename__ = 'department'
#
#     id = Column(Integer, primary_key=True)
#     code = Column(Integer)
#     description = Column(String)
#
# class Function(Base):
#     __tablename__ = 'function'
#
#     id = Column(Integer, primary_key=True)
#     code = Column(Integer)
#     description = Column(String)
#
# class LabourAgreementSettings(Base):
#     __tablename__ = 'labour_agreement_settings'
#
#     id = Column(Integer, primary_key=True)
#     guid = Column(String)
#     int_number = Column(Integer)
#     str_name = Column(String)
#     debtor_id = Column(Integer, ForeignKey('debtor.id'))
#     debtor = relationship("Debtor")
#
# class Manager(Base):
#     __tablename__ = 'manager'
#
#     id = Column(Integer, primary_key=True)
#     number = Column(Integer)
#     first_name = Column(String)
#     name = Column(String)
#     department = Column(String)
#     function = Column(String)
#     phone_number = Column(String)
#     mobile = Column(String)
#     fax = Column(String)
#     email = Column(String)
#
# class ServiceLevel(Base):
#     __tablename__ = 'service_level'
#
#     id = Column(Integer, primary_key=True)
#     start_period = Column(Integer)
#     start_year = Column(Integer)
#     service_level = Column(String)
#     start_contract = Column(DateTime)