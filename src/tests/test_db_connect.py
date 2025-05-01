from mongo_client import mongo_client


def test_db_health_check():
    is_database_working = True

    try:
        # to check database we will execute raw query
        res = mongo_client.db.command("dbstats")
    except Exception as e:
        print(str(e))
        is_database_working = False

    assert res["ok"] == 1
    assert is_database_working
