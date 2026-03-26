import os
import sys

# _web_test_utils を絶対インポートで参照できるようにする
_WEB_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
if _WEB_TEST_DIR not in sys.path:
    sys.path.insert(0, _WEB_TEST_DIR)
