"""Firestore MongoDB API: CRUD operations via pymongo."""

from datetime import datetime

from bson.objectid import ObjectId


class TestInsert:
    def test_insert_one(self, collection):
        result = collection.insert_one({"name": "test", "value": 1})
        assert result.inserted_id is not None

        doc = collection.find_one({"_id": result.inserted_id})
        assert doc["name"] == "test"
        assert doc["value"] == 1

    def test_insert_many(self, collection):
        docs = [{"name": f"item_{i}", "value": i} for i in range(5)]
        result = collection.insert_many(docs)
        assert len(result.inserted_ids) == 5
        assert collection.count_documents({}) == 5

    def test_insert_with_objectid(self, collection):
        _id = ObjectId()
        collection.insert_one({"_id": _id, "name": "explicit_id"})
        doc = collection.find_one({"_id": _id})
        assert doc is not None
        assert isinstance(doc["_id"], ObjectId)

    def test_insert_with_datetime(self, collection):
        now = datetime.utcnow()
        collection.insert_one({"created_at": now, "name": "datetime_test"})
        doc = collection.find_one({"name": "datetime_test"})
        assert isinstance(doc["created_at"], datetime)

    def test_insert_with_nested_dict(self, collection):
        collection.insert_one({
            "scores": {"U1": 25000, "U2": 30000},
            "meta": {"round": 1},
        })
        doc = collection.find_one({})
        assert doc["scores"]["U1"] == 25000

    def test_insert_with_objectid_reference(self, collection):
        """ObjectId cross-reference (like match_id in hanchans)."""
        ref_id = ObjectId()
        collection.insert_one({"match_id": ref_id, "name": "hanchan"})
        doc = collection.find_one({"match_id": ref_id})
        assert doc is not None
        assert doc["match_id"] == ref_id


class TestFind:
    def test_find_one(self, collection):
        collection.insert_one({"name": "target"})
        doc = collection.find_one({"name": "target"})
        assert doc is not None

    def test_find_multiple(self, collection):
        collection.insert_many([
            {"group": "A", "value": 1},
            {"group": "A", "value": 2},
            {"group": "B", "value": 3},
        ])
        results = list(collection.find({"group": "A"}))
        assert len(results) == 2

    def test_find_with_sort(self, collection):
        collection.insert_many([
            {"name": "c", "order": 3},
            {"name": "a", "order": 1},
            {"name": "b", "order": 2},
        ])
        results = list(collection.find().sort("order", 1))
        assert [r["name"] for r in results] == ["a", "b", "c"]

    def test_find_with_limit(self, collection):
        collection.insert_many([{"i": i} for i in range(10)])
        results = list(collection.find().limit(3))
        assert len(results) == 3

    def test_count_documents(self, collection):
        collection.insert_many([{"i": i} for i in range(7)])
        assert collection.count_documents({}) == 7
        assert collection.count_documents({"i": {"$gte": 5}}) == 2


class TestUpdate:
    def test_update_one_set(self, collection):
        _id = collection.insert_one({"name": "old"}).inserted_id
        result = collection.update_one({"_id": _id}, {"$set": {"name": "new"}})
        assert result.modified_count == 1
        assert collection.find_one({"_id": _id})["name"] == "new"

    def test_update_many(self, collection):
        collection.insert_many([
            {"group": "A", "done": False},
            {"group": "A", "done": False},
            {"group": "B", "done": False},
        ])
        result = collection.update_many(
            {"group": "A"},
            {"$set": {"done": True}},
        )
        assert result.modified_count == 2

    def test_update_unset(self, collection):
        _id = collection.insert_one({"name": "test", "old_field": 123}).inserted_id
        collection.update_one({"_id": _id}, {"$unset": {"old_field": ""}})
        doc = collection.find_one({"_id": _id})
        assert "old_field" not in doc

    def test_update_set_and_unset_combined(self, collection):
        """Migration pattern: set new field + unset old field."""
        _id = collection.insert_one({"status": 0}).inserted_id
        collection.update_one(
            {"_id": _id},
            {"$set": {"is_deleted": True}, "$unset": {"status": ""}},
        )
        doc = collection.find_one({"_id": _id})
        assert doc["is_deleted"] is True
        assert "status" not in doc


class TestDelete:
    def test_delete_one(self, collection):
        _id = collection.insert_one({"name": "to_delete"}).inserted_id
        result = collection.delete_one({"_id": _id})
        assert result.deleted_count == 1
        assert collection.find_one({"_id": _id}) is None

    def test_delete_many(self, collection):
        collection.insert_many([
            {"group": "del", "i": 1},
            {"group": "del", "i": 2},
            {"group": "keep", "i": 3},
        ])
        result = collection.delete_many({"group": "del"})
        assert result.deleted_count == 2
        assert collection.count_documents({}) == 1
