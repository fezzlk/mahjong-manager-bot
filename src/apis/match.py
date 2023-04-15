from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from xml.dom import NotFoundErr
from use_cases.web.GetMatchForWebUseCase import GetMatchForWebUseCase
# from use_cases.web.GetMatchesForWebUseCase import GetMatchesForWebUseCase
from use_cases.web.DeleteMatchesForWebUseCase import DeleteMatchesForWebUseCase
from use_cases.web.UpdateMatchForWebUseCase import UpdateMatchForWebUseCase
from flask_jwt_extended import jwt_required, get_jwt_identity
from ApplicationModels.EnhancedJSONEncoder import EnhancedJSONEncoder
import json
from repositories import (
    web_user_repository, user_group_repository, match_repository, session_scope
)

match_blueprint = Blueprint(
    'match_blueprint',
    __name__,
    url_prefix='/_api/match'
)


@match_blueprint.route('/')
@jwt_required()
def get_users():
    request_user_id = get_jwt_identity()

    with session_scope() as db_session:
        request_user = web_user_repository.find_by_id(
            session=db_session, id=request_user_id
        )

        if request_user.is_approved_line_user is False:
            return '失敗: LINEアカウント連携が完了していません。'

        line_groups = user_group_repository.find_by_line_user_id(
            session=db_session, line_user_id=request_user.linked_line_user_id
        )

        line_group_ids = [ug.line_group_id for ug in line_groups]

        matches = match_repository.find_many_by_line_group_ids_and_status(
            session=db_session,
            line_group_ids=line_group_ids,
            status=2
        )

    return json.dumps(matches, cls=EnhancedJSONEncoder)


# @match_blueprint.route('/')
# def get_matches():
#     data = GetMatchesForWebUseCase().execute()
#     keys = [
#         '_id',
#         'line_group_id',
#         'hanchan_ids',
#         'created_at',
#         'status',
#         'tip_scores',
#         'users']
#     input_keys = ['line_group_id', 'hanchan_ids', 'status']
#     return render_template(
#         'model.html',
#         title='matches',
#         submit_to='create_match',
#         keys=keys,
#         input_keys=input_keys,
#         data=data
#     )


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
