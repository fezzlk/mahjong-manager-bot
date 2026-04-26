"""Firestore MongoDB API: connection and basic operations."""


class TestConnection:
    def test_ping(self, firestore_client):
        result = firestore_client.admin.command("ping")
        assert result.get("ok") == 1.0

    def test_list_collection_names(self, firestore_db):
        names = firestore_db.list_collection_names()
        assert isinstance(names, list)

    def test_database_name(self, firestore_db):
        assert firestore_db.name is not None
