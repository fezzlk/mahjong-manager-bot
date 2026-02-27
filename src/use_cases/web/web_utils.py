import json
from enum import Enum
from typing import Any, Iterable, List, Optional, Type, TypeVar, Union

from bson.objectid import ObjectId

T = TypeVar("T")


def to_object_id(value: Union[str, ObjectId, int, None]) -> Union[ObjectId, int, None]:
    if value is None:
        return None
    if isinstance(value, ObjectId):
        return value
    if isinstance(value, str) and ObjectId.is_valid(value):
        return ObjectId(value)
    return value


def normalize_ids(values: Iterable[Union[str, ObjectId, int]]) -> List[Union[ObjectId, int]]:
    return [to_object_id(v) for v in values]


def delete_by_ids(repository: Any, ids: Iterable[Union[str, ObjectId, int]]) -> None:
    repository.delete({"_id": {"$in": normalize_ids(ids)}})


def find_one_by_id(repository: Any, _id: Union[str, ObjectId, int, None]) -> Optional[Any]:
    records = repository.find({"_id": to_object_id(_id)})
    return first_or_none(records)


def first_or_none(values: List[T]) -> Optional[T]:
    return values[0] if len(values) > 0 else None


def without_id(values: dict) -> dict:
    return {k: v for k, v in values.items() if k != "_id"}


def parse_enum_value(value: Optional[str], enum_class: Type[Enum]) -> Optional[int]:
    if value is None:
        return None
    enum_name = value.split(".")[-1]
    if enum_name == "":
        return None
    return enum_class[enum_name].value


def parse_json_dict(value: Union[str, dict, None], default: Optional[dict] = None) -> dict:
    if value is None or value == "":
        return {} if default is None else default
    if isinstance(value, dict):
        return value
    return json.loads(value.replace("'", '"'))


def parse_int_list(value: Union[str, List[int]]) -> Optional[List[int]]:
    if value is None:
        return None
    if isinstance(value, list):
        return [int(v) for v in value]
    if isinstance(value, str):
        if value.strip() == "":
            return []
        return [int(v.strip()) for v in value.replace("/", ",").split(",") if v.strip() != ""]
    return None
