"""Firestore MongoDB API: query operator and index compatibility.

Tests the specific pymongo query patterns used by the application
and migration scripts.
"""


import pymongo
import pytest
from bson.objectid import ObjectId


class TestQueryOperators:
    """Query operators used throughout the application."""

    def test_ne_operator(self, collection):
        """$ne is used by hanchan_repository.find() for is_deleted filtering."""
        collection.insert_many([
            {"is_deleted": True, "name": "deleted"},
            {"is_deleted": False, "name": "active"},
            {"name": "no_field"},
        ])
        results = list(collection.find({"is_deleted": {"$ne": True}}))
        names = {r["name"] for r in results}
        assert names == {"active", "no_field"}

    def test_exists_operator(self, collection):
        """$exists is used by migration scripts to check field presence."""
        collection.insert_many([
            {"status": 0, "name": "with_status"},
            {"name": "no_status"},
        ])
        with_status = list(collection.find({"status": {"$exists": True}}))
        assert len(with_status) == 1
        assert with_status[0]["name"] == "with_status"

        without_status = list(collection.find({"status": {"$exists": False}}))
        assert len(without_status) == 1

    def test_in_operator(self, collection):
        collection.insert_many([
            {"status": 0}, {"status": 1}, {"status": 2},
        ])
        results = list(collection.find({"status": {"$in": [0, 2]}}))
        assert len(results) == 2

    def test_gte_lte_operators(self, collection):
        collection.insert_many([{"value": i} for i in range(10)])
        results = list(collection.find({"value": {"$gte": 3, "$lte": 7}}))
        assert len(results) == 5

    def test_or_operator(self, collection):
        """$or is used by migrate_tip_to_chip.py for remaining check."""
        collection.insert_many([
            {"tip_scores": {"U1": 10}},
            {"chip_scores": {"U1": 10}},
            {"other": True},
        ])
        results = list(collection.find({
            "$or": [
                {"tip_scores": {"$exists": True}},
                {"chip_scores": {"$exists": True}},
            ],
        }))
        assert len(results) == 2

    def test_combined_exists_conditions(self, collection):
        """Migration pattern: find docs with old field but not new field."""
        collection.insert_many([
            {"status": 0},
            {"status": 2, "is_deleted": False},
            {"is_deleted": True},
        ])
        results = list(collection.find({
            "status": {"$exists": True},
            "is_deleted": {"$exists": False},
        }))
        assert len(results) == 1
        assert results[0]["status"] == 0


class TestUpdateOperators:
    """Update operators used by migration scripts."""

    def test_rename_operator(self, collection):
        """$rename is used by migrate_tip_to_chip.py."""
        _id = collection.insert_one({
            "tip_scores": {"U1": 10},
            "tip_prices": {"U1": 300},
            "sum_prices_with_tip": {"U1": 3300},
        }).inserted_id

        collection.update_one(
            {"_id": _id},
            {"$rename": {
                "tip_scores": "chip_scores",
                "tip_prices": "chip_prices",
                "sum_prices_with_tip": "sum_prices_with_chip",
            }},
        )

        doc = collection.find_one({"_id": _id})
        assert "chip_scores" in doc
        assert "chip_prices" in doc
        assert "sum_prices_with_chip" in doc
        assert "tip_scores" not in doc
        assert doc["chip_scores"] == {"U1": 10}

    def test_rename_via_update_many(self, collection):
        """Batch rename across multiple documents."""
        collection.insert_many([
            {"tip_rate": 30, "group": "A"},
            {"tip_rate": 50, "group": "B"},
            {"chip_rate": 10, "group": "C"},
        ])

        result = collection.update_many(
            {"tip_rate": {"$exists": True}},
            {"$rename": {"tip_rate": "chip_rate"}},
        )
        assert result.modified_count == 2

        for doc in collection.find({"group": {"$in": ["A", "B"]}}):
            assert "chip_rate" in doc
            assert "tip_rate" not in doc

    def test_set_and_unset_via_update_many(self, collection):
        """Migration pattern: status→is_deleted across all docs."""
        collection.insert_many([
            {"status": 0, "name": "disabled"},
            {"status": 2, "name": "archived"},
        ])

        # status=0 → is_deleted=True
        collection.update_many(
            {"status": 0, "is_deleted": {"$exists": False}},
            {"$set": {"is_deleted": True}, "$unset": {"status": ""}},
        )
        # status!=0 → is_deleted=False
        collection.update_many(
            {"status": {"$exists": True}, "is_deleted": {"$exists": False}},
            {"$set": {"is_deleted": False}, "$unset": {"status": ""}},
        )

        for doc in collection.find():
            assert "status" not in doc
            assert "is_deleted" in doc

        disabled = collection.find_one({"name": "disabled"})
        assert disabled["is_deleted"] is True
        archived = collection.find_one({"name": "archived"})
        assert archived["is_deleted"] is False

    def test_insert_many_ordered_false(self, collection):
        """insert_many(ordered=False) is used by migrate_atlas_to_firestore.py."""
        docs = [{"_id": ObjectId(), "i": i} for i in range(5)]
        result = collection.insert_many(docs, ordered=False)
        assert len(result.inserted_ids) == 5


class TestIndexOperations:
    """Index creation (used by setup_indexes.py).

    NOTE: create_index requires roles/datastore.indexAdmin, which is
    separate from roles/datastore.user. These tests verify the API
    compatibility but may fail with permission errors if the test user
    only has datastore.user role.
    """

    def test_create_index(self, collection):
        try:
            index_name = collection.create_index("line_group_id")
        except pymongo.errors.OperationFailure as e:
            if "PermissionDenied" in str(e) or "datastore.indexes.create" in str(e):
                pytest.skip("datastore.indexes.create permission not granted")
            raise
        assert index_name is not None
        indexes = list(collection.list_indexes())
        field_names = [
            next(iter(idx["key"].keys()))
            for idx in indexes
            if "_id" not in idx["key"]
        ]
        assert "line_group_id" in field_names

    def test_create_compound_index(self, collection):
        try:
            index_name = collection.create_index([
                ("line_group_id", pymongo.ASCENDING),
                ("is_deleted", pymongo.ASCENDING),
            ])
        except pymongo.errors.OperationFailure as e:
            if "PermissionDenied" in str(e) or "datastore.indexes.create" in str(e):
                pytest.skip("datastore.indexes.create permission not granted")
            raise
        assert index_name is not None


class TestCollectionOperations:
    """Collection-level operations used during migration."""

    def test_drop_collection_not_supported(self, firestore_db):
        """Firestore MongoDB API does NOT support the 'drop' command.

        Migration scripts should use delete_many({}) instead of drop().
        """
        col = firestore_db["compat_test_drop"]
        col.delete_many({})  # ensure clean state
        col.insert_one({"tmp": True})
        assert col.count_documents({}) == 1

        with pytest.raises(pymongo.errors.OperationFailure, match="Unsupported command drop"):
            col.drop()

        # Cleanup: use delete_many instead
        col.delete_many({})
        assert col.count_documents({}) == 0

    def test_count_documents_empty(self, collection):
        assert collection.count_documents({}) == 0

    def test_find_on_empty_collection(self, collection):
        results = list(collection.find({}))
        assert results == []
