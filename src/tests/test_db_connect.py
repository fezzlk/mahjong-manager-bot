from db_setting import Session
session = Session()


def test_db_health_check():
    is_database_working = True

    try:
        # to check database we will execute raw query
        session.execute('SELECT 1')
    except Exception as e:
        print(str(e))
        is_database_working = False

    assert is_database_working
