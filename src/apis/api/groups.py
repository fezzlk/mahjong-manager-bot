from flask import jsonify, make_response

from repositories import (
    group_repository,
    match_repository,
    user_group_repository,
    user_hanchan_repository,
    user_repository,
)
from . import api_blueprint
from ._auth import assert_group_member, require_web_user


def _line_user_id_from_web_user(web_user):
    return web_user.linked_line_user_id


@api_blueprint.route("/groups", methods=["GET"])
@require_web_user
def get_groups(web_user):
    """ログインユーザーの参加グループ一覧"""
    line_user_id = _line_user_id_from_web_user(web_user)
    if not line_user_id:
        return jsonify([])

    # ユーザーが所属するグループ ID を取得
    user_groups = user_group_repository.find({"line_user_id": line_user_id})
    line_group_ids = [ug.line_group_id for ug in user_groups]

    groups = []
    for line_group_id in line_group_ids:
        found = group_repository.find({"line_group_id": line_group_id})
        if not found:
            continue
        g = found[0]
        # メンバー数取得
        members = user_group_repository.find({"line_group_id": line_group_id})
        groups.append({
            "id": str(g._id),
            "name": line_group_id,  # Group には name フィールドがないため line_group_id を使用
            "description": None,
            "member_count": len(members),
        })

    return jsonify(groups)


@api_blueprint.route("/groups/<group_id>", methods=["GET"])
@require_web_user
def get_group(web_user, group_id):
    """グループ詳細"""
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        groups = group_repository.find({"_id": ObjectId(group_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not groups:
        return make_response(jsonify({"error": "Not found"}), 404)

    g = groups[0]
    err = assert_group_member(web_user, g.line_group_id)
    if err:
        return err

    members = user_group_repository.find({"line_group_id": g.line_group_id})

    member_list = []
    for ug in members:
        users = user_repository.find({"line_user_id": ug.line_user_id})
        member_list.append({
            "line_user_id": ug.line_user_id,
            "name": users[0].line_user_name if users else ug.line_user_id,
        })

    return jsonify({
        "id": str(g._id),
        "name": g.line_group_id,
        "description": None,
        "member_count": len(members),
        "members": member_list,
    })
