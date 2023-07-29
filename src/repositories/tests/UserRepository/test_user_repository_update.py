from repositories import user_repository
from DomainModel.entities.User import User, UserMode


before = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)
after = User(
    line_user_name="test_user2",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user2",
)


def test_hit_1_record():
    # Arrange
    user_repository.create(
        before
    )

    # Act
    user_repository.update(
        query={'line_user_id': before.line_user_id},
        new_values={
            'line_user_name': after.line_user_name,
            'jantama_name': after.jantama_name,
        },
    )

    # Assert
    result = user_repository.find()[0]
    assert isinstance(result, User)
    assert result.line_user_name == after.line_user_name
    assert result.line_user_id == after.line_user_id
    assert result.mode == after.mode
    assert result.jantama_name == after.jantama_name
