from flask import make_response
from json import dumps, loads
from uuid import UUID


class IncorrectValueException(Exception):
    pass


class JSONData:
    def __init__(self, json: bytes):
        json = loads(json)
        uuid = json.get('addition', {}).get('uuid')
        self._uuid = UUID(uuid, version=4)

        name = json.get('name')
        if name:
            self._name = name

        value = json.get('addition', {}).get('value')
        if value:
            if value < 0:
                raise IncorrectValueException('Value parameter should be positive.')
            self._value = value

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def value(self):
        if not self._value:
            raise IncorrectValueException('Value parameter can not be None for this type of request.')
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
