"""
api
"""

from server import app

@app.route('/_api/results')
def api_get_results():
    # Results.get_json(Engine)
    # data = services.results_service.get()
    # print(data)
    # print(type(data))
    return 'hoge'