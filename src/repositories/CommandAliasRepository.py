from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import command_aliases_collection
from DomainModel.entities.CommandAlias import CommandAlias
from DomainModel.IRepositories.ICommandAliasRepository import ICommandAliasRepository


class CommandAliasRepository(ICommandAliasRepository):

    def create(
        self,
        new_record: CommandAlias,
    ) -> CommandAlias:
        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop('_id')
        result = command_aliases_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = command_aliases_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[CommandAlias]:
        records = command_aliases_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = command_aliases_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> CommandAlias:
        return CommandAlias(
            line_user_id=record.get("line_user_id"),
            line_group_id=record.get("line_group_id"),
            alias=record.get("alias"),
            command=record.get("command"),
            mentionees=record.get("mentionees"),
            created_at=record.get('created_at'),
            updated_at=record.get('updated_at'),
            _id=record.get('_id'),
        )
