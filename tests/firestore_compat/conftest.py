"""Firestore MongoDB compatibility test fixtures.

These tests require a real Firestore database with MongoDB API enabled.
Set FIRESTORE_TEST_DATABASE_URL to run them.

Usage:
  FIRESTORE_TEST_DATABASE_URL="mongodb://..." pytest tests/firestore_compat/ -v

  Or set FIRESTORE_TEST_DATABASE_NAME to override the default test DB name.
"""

import contextlib
import os

import pytest
from pymongo import MongoClient

FIRESTORE_URL = os.environ.get("FIRESTORE_TEST_DATABASE_URL")
FIRESTORE_DB_NAME = os.environ.get("FIRESTORE_TEST_DATABASE_NAME", "mahjong-manager-test")

# Test collection name (isolated to avoid conflicts)
TEST_COLLECTION = "compat_test"


def pytest_collection_modifyitems(config, items):
    """Skip all tests in this directory if FIRESTORE_TEST_DATABASE_URL is not set."""
    if FIRESTORE_URL:
        return
    skip = pytest.mark.skip(reason="FIRESTORE_TEST_DATABASE_URL not set")
    for item in items:
        item.add_marker(skip)


@pytest.fixture(scope="session")
def firestore_client():
    """Session-scoped Firestore MongoDB client."""
    client = MongoClient(FIRESTORE_URL)
    yield client
    client.close()


@pytest.fixture(scope="session")
def firestore_db(firestore_client):
    """Session-scoped Firestore test database."""
    return firestore_client[FIRESTORE_DB_NAME]


@pytest.fixture
def collection(firestore_db):
    """Function-scoped test collection, cleaned up after each test."""
    col = firestore_db[TEST_COLLECTION]
    with contextlib.suppress(Exception):
        col.delete_many({})
    yield col
    with contextlib.suppress(Exception):
        col.delete_many({})
