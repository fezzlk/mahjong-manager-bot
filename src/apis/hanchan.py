# from flask import (
#     Blueprint,
#     redirect,
#     request,
#     render_template,
#     url_for,
# )
# from xml.dom import NotFoundErr
# from use_cases.web.GetHanchanForWebUseCase import GetHanchanForWebUseCase
# # from use_cases.web.GetHanchansForWebUseCase import GetHanchansForWebUseCase
# from use_cases.web.UpdateHanchanForWebUseCase import UpdateHanchanForWebUseCase
# from use_cases.web.DeleteHanchansForWebUseCase import DeleteHanchansForWebUseCase
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from ApplicationModels.EnhancedJSONEncoder import EnhancedJSONEncoder
# import json
# from repositories import (
#     web_user_repository, user_group_repository, hanchan_repository, session_scope
# )

# hanchan_blueprint = Blueprint(
#     'hanchan_blueprint',
#     __name__,
#     url_prefix='/_api/hanchan'
# )

# @hanchan_blueprint.route('/')
# @jwt_required()
# def get_users():
#     request_user_id = get_jwt_identity()

#     request_user = web_user_repository.find_by_id(
#         session=db_session, _id=request_user_id
#     )

#     if request_user.is_approved_line_user is False:
#         return '失敗: LINEアカウント連携が完了していません。'

#     line_groups = user_group_repository.find_by_line_user_id(
#         session=db_session, line_user_id=request_user.linked_line_user_id
#     )

#     line_group_ids = [ug.line_group_id for ug in line_groups]

#     hanchans = hanchan_repository.find_many_by_line_group_ids_and_status(
#         session=db_session,
#         line_group_ids=line_group_ids,
#         status=2
#     )

#     return json.dumps(hanchans, cls=EnhancedJSONEncoder)

# # @hanchan_blueprint.route('/')
# # def get_hanchans():
# #     data = GetHanchansForWebUseCase().execute()
# #     keys = ['_id', 'line_group_id', 'raw_scores',
# #             'converted_scores', 'match_id', 'status']
# #     input_keys = ['line_group_id', 'raw_scores',
# #                   'converted_scores', 'match_id', 'status']
# #     return render_template(
# #         'model.html',
# #         title='hanchans',
# #         submit_to='create_hanchan',
# #         keys=keys,
# #         input_keys=input_keys,
# #         data=data
# #     )


# @hanchan_blueprint.route('/<_id>')
# def hanchans_detail(_id):
#     data = GetHanchanForWebUseCase().execute(_id)
#     if data is None:
#         raise NotFoundErr()
#     input_keys = ['_id', 'line_group_id', 'raw_scores',
#                   'converted_scores', 'match_id', 'status']
#     return render_template(
#         'detail.html',
#         title='hanchans',
#         submit_to='update_hanchan',
#         input_keys=input_keys,
#         init_data=data
#     )


# @hanchan_blueprint.route('/create', methods=['POST'])
# def create_hanchan():
#     return redirect(url_for('views_blueprint.get_hanchans'))


# @hanchan_blueprint.route('/update', methods=['POST'])
# def update_hanchan():
#     UpdateHanchanForWebUseCase().execute()
#     return redirect(url_for('views_blueprint.get_hanchans'))


# @hanchan_blueprint.route('/delete', methods=['POST'])
# def delete_hanchans():
#     target_id = request.args.get('target_id')
#     DeleteHanchansForWebUseCase().execute([int(target_id)])
#     return redirect(url_for('views_blueprint.get_hanchans'))
