from flask import make_response
from json import dumps, loads
from uuid import UUID


class IncorrectParameterException(Exception):
    pass


class JSONData:
    """
    Class to work with JSON.
    """
    def __init__(self, json: bytes):
        json = loads(json.decode())
        uuid = json.get('addition', {}).get('uuid')
        if not uuid:
            raise IncorrectParameterException('Parameter `uuid` is empty.')
        self._uuid = UUID(uuid, version=4)
        self._value = json.get('addition', {}).get('value')

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def value(self):
        if self._value is None:
            raise IncorrectParameterException(
                'Parameter `value` can not be `None` for this type of request.'
            )
        else:
            self._value = float(self._value)
            if self._value < 0:
                raise IncorrectParameterException(
                    'Parameter `value` should be non-negative.'
                )
            return self._value


def form_response(status: int, result: bool, uuid: str = None, name: str = None, addition: dict = None,
                  description: dict = None):
    result_dict = {
        'status': status,
        'result': result,
        'addition': {},
        'description': {}
    }
    if uuid:
        result_dict['addition'].update(dict(uuid=uuid))
    if name:
        result_dict['addition'].update(dict(name=name))
    if addition:
        result_dict['addition'].update(addition)
    if description:
        result_dict['description'].update(description)
    return make_response(dumps(result_dict), status)
