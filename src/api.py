"""
api
"""

from server import app
from use_cases import (
    hanchans_use_cases,
)
from db_setting import Engine
from models import Results


@app.route('/_api/results')
def api_get_results():
    """get results

    Returns:
        data: results list
    """
    Results.get_json(Engine)
    data = hanchans_use_cases.get()
    print(data)
    print(type(data))
    return data
