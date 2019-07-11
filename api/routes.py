from functools import wraps

from flask import request

from api import app
from api.utils import JSONData, form_response
from db.queries import add_sum, UUIDNotExistException, ClosedBankAccountExeption, get_status


def safe_wrapper(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        try:
            route_func(*args, **kwargs)
        except ValueError as e:
            return form_response(400, False, description=dict(error=str(e)))
        except ClosedBankAccountExeption as e:
            return form_response(403, False, description=dict(error=str(e)))
        except UUIDNotExistException as e:
            return form_response(404, False, description=dict(error=str(e)))
        return wrapper


@app.route('/api/ping')
def ping():
    return form_response(200, True)


@safe_wrapper
@app.route('/api/add')
def add():
    json_data = JSONData(request.data)
    add_sum(json_data.uuid, json_data.value)
    return form_response(200, True, json_data.uuid)


@safe_wrapper
@app.route('/api/subtract')
@app.route('/api/substract')
def subtract():
    pass


@safe_wrapper
@app.route('/api/status')
def status():
    json_data = JSONData(request.data)
    balance, status = get_status(json_data.uuid)
    return form_response(200, True, json_data.uuid, addition=dict(balance=balance, status=status))
