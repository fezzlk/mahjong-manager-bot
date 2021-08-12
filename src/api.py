"""
api
"""

from server import app, Engine

    """get results

    Returns:
        data: results list
    """
@app.route('/_api/results')
def api_get_results():
    Results.get_json(Engine)
    data = services.results_service.get()
    print(data)
    print(type(data))
    return data