from os.path import join, splitext
from typing import Any, FrozenSet
from uuid import uuid4

from flask import jsonify, make_response, request
from flask.views import MethodView
from flask.wrappers import Response
from flask_api import status
from returns.pipeline import is_successful

import helpers
import settings as se

from ..models.connector import DatabaseConnector
from ..models.employee import EmployeeModel
from . import employee_blueprint


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


class EmployeesView(MethodView):

    def get(self) -> Response:
        """GET method for get all Employees."""
        with DatabaseConnector(se.DatabaseEngines.SQLITE) as dbs:
            if dbs.enter_to_context:
                employee_model = EmployeeModel(dbs.session)
                employees = employee_model.get_employees()
                return make_response(jsonify(message='All employees',
                                             payload=[employee.json() for employee in employees]),
                                     status.HTTP_200_OK)
        return make_response(jsonify({}), status.HTTP_204_NO_CONTENT)

    def post(self) -> Response:
        """POST method for create new Employee.

        Require fields:
            first_name, last_name, in_company_from, photography
        """
        request_data_result = helpers.from_request(request.data)
        if not is_successful(request_data_result):
            return make_response(jsonify(message='JSON decode error'),
                                 status.HTTP_400_BAD_REQUEST)
        request_data = request_data_result.unwrap()
        # Check for missing require fields
        fields: FrozenSet[str] = \
            frozenset(('first_name', 'last_name', 'in_company_from', 'photography'))
        if not helpers.require_fields(request_data, fields):
            return make_response(jsonify(message='Please, fill out all the require fields'),
                                 status.HTTP_400_BAD_REQUEST)
        photography = request_data.get('photography')
        # Upload file process
        offset = (se.shared.EMPLOYEE_PHOTO_WIDTH, se.shared.EMPLOYEE_PHOTO_HEIGHT)
        file_name = \
            helpers.upload_ib64(join(se.shared.PHOTOS_DIR, f'{uuid4().hex}'), photography, offset)
        if is_successful(file_name):
            # If upload file is well, - update new employee fields
            *_, static, photo = join(se.shared.PHOTOS_DIR, file_name.unwrap()).rpartition('/static')
            request_data.update({'photography': f'{static}{photo}'})
        with DatabaseConnector(se.DatabaseEngines.SQLITE) as dbs:
            if dbs.enter_to_context:
                employee_model = EmployeeModel(dbs.session)
                employee_model.create(request_data)
                return make_response(jsonify(message='Employee was added', payload=employee_model.json()),
                                     status.HTTP_200_OK)
        return make_response(jsonify({}), status.HTTP_204_NO_CONTENT)

    def delete(self, id: int) -> Response:
        """DELETE method for delete Employee.

        Args:
            id: Employee id to be deleted
        """
        with DatabaseConnector(se.DatabaseEngines.SQLITE) as dbs:
            if dbs.enter_to_context:
                employee_model = EmployeeModel(dbs.session)
                employee = employee_model.get_employee(id)
                # First clean the user files
                helpers.remove_file(f'{se.shared.BASE_DIR}{employee.photography}')
                # ... and then delete the user
                employee_model.delete(id)
                return make_response(jsonify(message='Employee was deleted'),
                                     status.HTTP_200_OK)
        return make_response(jsonify({}), status.HTTP_204_NO_CONTENT)


# Register routes employees in Blueprint
routes = {
    '/v1/employee/fetch/': EmployeesView.as_view('employee_fetch'),
    '/v1/employee/create/': EmployeesView.as_view('employee_create'),
    '/v1/employee/<int:id>/delete/': EmployeesView.as_view('employee_delete')
}
for rule, view_func in routes.items():
    employee_blueprint.add_url_rule(rule=rule, view_func=view_func)
