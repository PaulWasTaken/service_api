from flask import make_response
from json import dumps, loads
from uuid import UUID


class JSONData:
    def __init__(self, json: bytes):
        json = loads(json)
        uuid = json.get('addition', {}).get('uuid')
        self._uuid = UUID(uuid, version=4)

        name = json.get('name')
        self._name = name
        self._value = json.get('addition', {}).get('value')

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def value(self):
        return self._value


def form_response(status: int, result: bool, uuid: str=None, name: str=None, addition: dict=None, description: dict=None):
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
