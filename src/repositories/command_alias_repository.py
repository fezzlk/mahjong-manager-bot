import copy
from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.command_alias import CommandAlias
from domain_model.i_repositories.i_command_alias_repository import ICommandAliasRepository
from mongo_client import command_aliases_collection


class CommandAliasRepository(ICommandAliasRepository):

    def create(
        self,
        new_record: CommandAlias,
    ) -> CommandAlias:
        new_dict = copy.deepcopy(new_record.__dict__)
        if new_record._id is None:
            new_dict.pop("_id")
        result = command_aliases_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values["updated_at"] = datetime.now()
        result = command_aliases_collection.update_one(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[CommandAlias]:
        records = command_aliases_collection\
            .find(filter=dict(query) if query is not None else {})\
            .sort(sort)\
            .limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = command_aliases_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> CommandAlias:
        return CommandAlias(
            line_user_id=record.get("line_user_id"),
            line_group_id=record.get("line_group_id"),
            alias=record.get("alias"),
            command=record.get("command"),
            mentionees=record.get("mentionees"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
