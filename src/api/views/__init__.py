from flask import Blueprint


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


employee_blueprint = Blueprint('employee_blueprint', __name__)

from .employee import *
