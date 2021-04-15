from typing import Any, Dict, Optional, Sequence

from pendulum import now, instance
from sqlalchemy import Column, DateTime, Integer, MetaData, String
from sqlalchemy.engine.result import ResultProxy, RowProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.scoping import ScopedSession


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


__all__: Sequence[str] = ('EmployeeModel',)

# Vars definitions
_meta = MetaData()
Base = declarative_base(metadata=_meta)


class EmployeeModel(Base):  # type: ignore
    """The Employee model."""

    __tablename__ = 'employee'
    __repr_attrs__ = ['first_name', 'last_name']

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    in_company_from = Column(String(16), nullable=False)
    photography = Column(String(512), nullable=True, default='')

    create_on = Column(DateTime(), nullable=False)

    def __init__(self, dbs: ScopedSession) -> None:
        """Create a new employee model."""
        self._dbs  = dbs

    def create(self, fields: Dict[str, Any]) -> None:
        """Create simple employee."""
        # Filling model
        self.first_name = fields.get('first_name')
        self.last_name = fields.get('last_name')
        self.in_company_from = fields.get('in_company_from')
        self.photography = fields.get('photography')
        self.create_on = now()
        # ... and save her
        self._dbs.add(self)
        self._dbs.commit()

    def delete(self, id: int) -> None:
        """Delete simple employee."""
        employee = \
            self._dbs.query(EmployeeModel).filter_by(id=id).one_or_none()
        if employee:
            self._dbs.delete(employee)
            self._dbs.commit()

    def get_employees(self) -> ResultProxy:
        """Return all employees."""
        return self._dbs.query(EmployeeModel).all()

    def get_employee(self, id: int) -> Optional[RowProxy]:
        """Return simple employee by ID."""
        return self._dbs.query(EmployeeModel).filter_by(id=id).one_or_none()

    def json(self) -> Dict[str, Any]:
        """Converts model to JSON format

        Returns:
            JSON formed from model fields
        """
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'in_company_from': self.in_company_from,
                'photography': self.photography,
                'create_on': instance(self.create_on).to_datetime_string()}
