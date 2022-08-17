import json

# import orjson as orjson
from pydantic import BaseModel
from pydantic.utils import to_camel

#
# def orjson_dumps(v, *, default):
#     # orjson.dumps returns bytes, to match standard json.dumps we need to decode
#     return orjson.dumps(v, default=default).decode()


class MyBaseModel(BaseModel):
    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_json(cls, j):
        return cls.from_dict(json.loads(j))

    def to_json(self):
        return self.json(by_alias=True)

    class Config:
        alias_generator = to_camel
        arbitrary_types_allowed = True
        # use_enum_values = True
        # by_alias = True
        # json_dumps = orjson_dumps
