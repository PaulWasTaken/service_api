from functools import wraps

from flask import request

from api import app
from api.utils import JSONData, form_response, IncorrectParameterException
from core.log import get_logger
from db.queries import add_sum, get_status, subtract_sum, \
    ClosedBankAccountExeption, NotEnoughMoney, UUIDNotFoundException

logger = get_logger('routes')


def safe_route_wrapper(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        try:
            return route_func(*args, **kwargs)
        except (IncorrectParameterException, ValueError) as e:
            # ValueError for bad UUID.
            logger.warning(str(e))
            return form_response(400, False, description=dict(error=str(e)))
        except ClosedBankAccountExeption as e:
            logger.info(str(e))
            return form_response(403, False, description=dict(error=str(e)))
        except UUIDNotFoundException as e:
            logger.info(str(e))
            return form_response(404, False, description=dict(error=str(e)))
        except NotEnoughMoney as e:
            logger.info(str(e))
            return form_response(406, False, description=dict(error=str(e)))
        except Exception as e:
            logger.error(str(e))
            return form_response(500, False, description=dict(error=str(e)))
    return wrapper


@app.route('/api/ping')
def ping():
    logger.debug('Ping was called.')
    return form_response(200, True)


@app.route('/api/add')
@safe_route_wrapper
def add():
    logger.debug('Add was called.')
    json_data = JSONData(request.data)
    add_sum(json_data.uuid, json_data.value)
    return form_response(200, True, json_data.uuid)


@app.route('/api/subtract')
@app.route('/api/substract')
@safe_route_wrapper
def subtract():
    logger.debug('Subtract was called.')
    json_data = JSONData(request.data)
    subtract_sum(json_data.uuid, json_data.value)
    return form_response(200, True, json_data.uuid)


@app.route('/api/status')
@safe_route_wrapper
def status():
    logger.debug('Status was called.')
    json_data = JSONData(request.data)
    balance, status = get_status(json_data.uuid)
    return form_response(200, True, json_data.uuid,
                         addition=dict(balance=balance, status=status))
