from functools import wraps

from flask import request

from api import app
from api.utils import JSONData, form_response, IncorrectValueException
from db.queries import add_sum, UUIDNotFoundException, ClosedBankAccountExeption, get_status, subtract_sum, \
    NotEnoughMoney


def safe_wrapper(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        try:
            return route_func(*args, **kwargs)
        except (IncorrectValueException, ValueError) as e:
            # Bad UUIDv4
            return form_response(400, False, description=dict(error=str(e)))
        except ClosedBankAccountExeption as e:
            return form_response(403, False, description=dict(error=str(e)))
        except UUIDNotFoundException as e:
            return form_response(404, False, description=dict(error=str(e)))
        except NotEnoughMoney as e:
            return form_response(406, False, description=dict(error=str(e)))
    return wrapper


@app.route('/api/ping')
def ping():
    return form_response(200, True)


@app.route('/api/add')
@safe_wrapper
def add():
    json_data = JSONData(request.data)
    add_sum(json_data.uuid, json_data.value)
    return form_response(200, True, json_data.uuid)


@app.route('/api/subtract')
@app.route('/api/substract')
@safe_wrapper
def subtract():
    json_data = JSONData(request.data)
    subtract_sum(json_data.uuid, json_data.value)
    return form_response(200, True, json_data.uuid)


@app.route('/api/status')
@safe_wrapper
def status():
    json_data = JSONData(request.data)
    balance, status = get_status(json_data.uuid)
    return form_response(200, True, json_data.uuid, addition=dict(balance=balance, status=status))
