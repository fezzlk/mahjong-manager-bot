from domains.config import Config
import os
TEST_USER_ID = os.environ["TEST_USER_ID"]


def generateMockConfig():
    return Config(
        TEST_USER_ID,
        '飛び賞',
        '10',
    )
