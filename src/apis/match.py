from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from xml.dom import NotFoundErr
from use_cases.web.GetMatchForWebUseCase import GetMatchForWebUseCase
from use_cases.web.GetMatchesForWebUseCase import GetMatchesForWebUseCase
from use_cases.web.DeleteMatchesForWebUseCase import DeleteMatchesForWebUseCase
from use_cases.web.UpdateMatchForWebUseCase import UpdateMatchForWebUseCase

match_blueprint = Blueprint(
    'match_blueprint',
    __name__,
    url_prefix='/match'
)


@match_blueprint.route('/')
def get_matches():
    data = GetMatchesForWebUseCase().execute()
    keys = [
        '_id',
        'line_group_id',
        'hanchan_ids',
        'created_at',
        'status',
        'tip_scores',
        'users']
    input_keys = ['line_group_id', 'hanchan_ids', 'status']
    return render_template(
        'model.html',
        title='matches',
        submit_to='create_match',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@match_blueprint.route('/<_id>')
def matches_detail(_id):
    data = GetMatchForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'line_group_id', 'hanchan_ids', 'status']
    return render_template(
        'detail.html',
        title='matches',
        submit_to='update_match',
        input_keys=input_keys,
        init_data=data
    )


@match_blueprint.route('/create', methods=['POST'])
def create_match():
    return redirect(url_for('views_blueprint.get_matches'))


@match_blueprint.route('/update', methods=['POST'])
def update_match():
    UpdateMatchForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_matches'))


@match_blueprint.route('/delete', methods=['POST'])
def delete_matches():
    target_id = request.args.get('target_id')
    DeleteMatchesForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_matches'))
