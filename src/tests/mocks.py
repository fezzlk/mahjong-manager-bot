import os
TEST_USER_ID = os.environ["TEST_USER_ID"]


class MockConfig:
    def __init__(
        self,
        target_id=TEST_USER_ID,
        key='飛び賞',
        value='10',
    ):
        self.target_id = target_id
        self.key = key
        self.value = value
