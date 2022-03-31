from DomainModel.entities.Config import Config
from repositories import session_scope, config_repository


dummy_configs = [
    Config(
        target_id="U0123456789abcdefghijklmnopqrstu1",
        key='飛び賞',
        value='30',
        _id=1,
    ),
    Config(
        target_id="U0123456789abcdefghijklmnopqrstu1",
        key='レート',
        value='点2',
        _id=1,
    )
]


def test_hit_1_record():
    # Arrange
    with session_scope() as session:
        config_repository.create(session, dummy_configs[0])

    # Act
    with session_scope() as session:
        result = config_repository.update(
            session=session,
            target=dummy_configs[1],
        )

    # Assert
    assert result == 1

    with session_scope() as session:
        record_on_db = config_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_configs[1]._id
        assert record_on_db[0].target_id == dummy_configs[1].target_id
        assert record_on_db[0].key == dummy_configs[1].key
        assert record_on_db[0].value == dummy_configs[1].value


def test_hit_0_record():
    # Arrange

    # Act
    with session_scope() as session:
        result = config_repository.update(
            session,
            dummy_configs[0],
        )

    # Assert
    assert result == 0
