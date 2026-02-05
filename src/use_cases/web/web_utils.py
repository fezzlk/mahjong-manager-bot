from typing import Iterable, List, Optional, Union

from bson.objectid import ObjectId


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


def without_id(values: dict) -> dict:
    return {k: v for k, v in values.items() if k != "_id"}


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
