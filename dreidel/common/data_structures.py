import json


class BorgMeta(type):
    _shared_state = {}

    def __call__(cls, *args, **kwds):
        obj = super().__call__(*args, **kwds)
        obj.__dict__ = cls._shared_state
        return obj


class DataObject:
    def serialize(self):
        json.dumps(self)
