# from flask import (
#     Blueprint,
#     # request,
#     # render_template,
#     # url_for,
#     # redirect,
# )
# import json
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from ApplicationModels.EnhancedJSONEncoder import EnhancedJSONEncoder
# # from xml.dom import NotFoundErr
# # from use_cases.web.GetUserForWebUseCase import GetUserForWebUseCase
# # from use_cases.web.GetUsersForWebUseCase import GetUsersForWebUseCase
# # from use_cases.web.UpdateUserForWebUseCase import UpdateUserForWebUseCase
# # from use_cases.web.DeleteUsersForWebUseCase import DeleteUsersForWebUseCase
# from middlewares import parse_jwt_token
# from repositories import (
#     web_user_repository, user_repository, session_scope
# )

# user_blueprint = Blueprint(
#     'user_blueprint',
#     __name__,
#     url_prefix='/_api/user'
# )


# @user_blueprint.route('/')
# @jwt_required()
# @parse_jwt_token
# def get_users():
#     request_user_id = get_jwt_identity()

#     with session_scope() as db_session:
#         request_user = web_user_repository.find_by_id(
#             session=db_session, _id=request_user_id
#         )

#         if request_user.is_approved_line_user is False:
#             return '失敗: LINEアカウント連携が完了していません。'

#         line_user = user_repository.find_one_by_line_user_id(
#             session=db_session, line_user_id=request_user.linked_line_user_id
#         )
#         if line_user is None:
#             return '失敗: LINEアカウントの取得に失敗しました。'

#         # related_hanchan = user_repository.get_related_hanchans(
#         #     session=db_session,
#         # )
#         result = 'done'
#     return json.dumps(result, cls=EnhancedJSONEncoder)

# # @user_blueprint.route('/')
# # def view_users():
# #     data = GetUsersForWebUseCase().execute()
# #     keys = ['_id', 'line_user_name', 'line_user_id', 'jantama_name',
# #             'mode', 'matches', 'groups']
# #     input_keys = [
# #         'line_user_name',
# #         'line_user_id',
# #         'jantama_name']
# #     return render_template(
# #         'model.html',
# #         title='users',
# #         submit_to='create_user',
# #         keys=keys,
# #         input_keys=input_keys,
# #         data=data
# #     )


# # @user_blueprint.route('/<_id>')
# # def users_detail(_id):
# #     data = GetUserForWebUseCase().execute(_id)
# #     if data is None:
# #         raise NotFoundErr()
# #     input_keys = [
# #         '_id',
# #         'line_user_name',
# #         'line_user_id',
# #         'mode',
# #         'jantama_name']
# #     return render_template(
# #         'detail.html',
# #         title='user_detail',
# #         submit_to='update_user',
# #         input_keys=input_keys,
# #         init_data=data
# #     )


# # @user_blueprint.route('/create', methods=['POST'])
# # def create_user():
# #     # line_user_name = request.form['line_user_name']
# #     # user_id = request.form['user_id']
# #     # user_use_cases.create(line_user_name, user_id)
# #     return redirect(url_for('views_blueprint.get_users'))


# # @user_blueprint.route('/update', methods=['POST'])
# # def update_user():
# #     UpdateUserForWebUseCase().execute()
# #     return redirect(url_for('views_blueprint.get_users'))


# # @user_blueprint.route('/delete', methods=['POST'])
# # def delete_users():
# #     target_id = request.args.get('target_id')
# #     DeleteUsersForWebUseCase().execute([int(target_id)])
# #     return redirect(url_for('views_blueprint.get_users'))
