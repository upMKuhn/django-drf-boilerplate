from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)


class JsonSerializable:
    def encode(self):
        pass

    @staticmethod
    def decode(request: dict):
        pass
