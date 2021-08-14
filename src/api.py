"""
api
"""

from server import app, services
from db_setting import Engine
from models import Results


@app.route('/_api/results')
def api_get_results():
    """get results

    Returns:
        data: results list
    """
    Results.get_json(Engine)
    data = services.results_service.get()
    print(data)
    print(type(data))
    return data
