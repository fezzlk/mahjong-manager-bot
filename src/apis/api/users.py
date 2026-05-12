from flask import jsonify, make_response, request, session
from flask_jwt_extended import create_access_token

from domain_model.entities.web_user import WebUser
from repositories import web_user_repository

from . import api_blueprint
from ._auth import require_web_user


@api_blueprint.route("/register-info", methods=["GET"])
def get_register_info():
    """LINE 認証後の新規登録フォーム用情報。セッションから LINE ユーザー情報を返す。"""
    line_user_id = session.get("login_line_user_id")
    if not line_user_id:
        return make_response(jsonify({"error": "No registration session"}), 401)
    return jsonify({
        "line_user_id": line_user_id,
        "name": session.get("login_name", ""),
    })


@api_blueprint.route("/register", methods=["POST"])
def register_web_user():
    """LINE 認証後の新規 WebUser 登録。JWT を発行して返す。"""
    line_user_id = session.get("login_line_user_id")
    if not line_user_id:
        return make_response(jsonify({"error": "No registration session"}), 401)

    body = request.get_json(silent=True) or {}
    name = body.get("name") or session.get("login_name", "")

    # 同じ LINE ユーザーで既に登録済みの場合は 409
    existing = web_user_repository.find({"linked_line_user_id": line_user_id})
    if existing:
        return make_response(jsonify({"error": "Already registered"}), 409)

    new_user = WebUser(
        user_code=line_user_id,
        name=name,
        linked_line_user_id=line_user_id,
    )
    web_user = web_user_repository.create(new_user)

    session.pop("login_line_user_id", None)
    session.pop("login_name", None)

    access_token = create_access_token(identity=str(web_user._id))
    return jsonify({"access_token": access_token}), 201


@api_blueprint.route("/me", methods=["GET"])
@require_web_user
def get_me(web_user):
    return jsonify({
        "id": str(web_user._id),
        "email": web_user.email,
        "name": web_user.name,
        "line_user_id": web_user.linked_line_user_id,
    })


@api_blueprint.route("/users/<user_id>", methods=["GET"])
@require_web_user
def get_user(web_user, user_id):
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        target_users = web_user_repository.find({"_id": ObjectId(user_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not target_users:
        return make_response(jsonify({"error": "Not found"}), 404)

    target = target_users[0]
    return jsonify({
        "id": str(target._id),
        "name": target.name,
        "email": target.email,
        "line_user_id": target.linked_line_user_id,
    })


@api_blueprint.route("/users/<user_id>/stats", methods=["GET"])
@require_web_user
def get_user_stats(web_user, user_id):
    """ユーザー個人統計。user_id='me' の場合はログインユーザー。"""
    from repositories import (  # noqa: PLC0415
        user_hanchan_repository,
    )

    if user_id == "me":
        line_user_id = web_user.linked_line_user_id
    else:
        from bson.objectid import ObjectId  # noqa: PLC0415
        try:
            target_users = web_user_repository.find({"_id": ObjectId(user_id)})
        except Exception:
            return make_response(jsonify({"error": "Not found"}), 404)
        if not target_users:
            return make_response(jsonify({"error": "Not found"}), 404)
        line_user_id = target_users[0].linked_line_user_id

    if not line_user_id:
        return jsonify({
            "total_hanchan": 0,
            "total_point": 0,
            "average_rank": 0,
            "rank_distribution": {"first": 0, "second": 0, "third": 0, "fourth": 0},
            "point_history": [],
        })

    group_id = request.args.get("group_id")
    if group_id:
        from domain_service import group_service  # noqa: PLC0415
        from repositories import hanchan_repository  # noqa: PLC0415
        effective_ids = group_service.get_effective_line_group_ids(group_id)
        hanchans = hanchan_repository.find({"line_group_id": {"$in": effective_ids}})
        hanchan_ids = [h._id for h in hanchans]
        user_hanchans = user_hanchan_repository.find({
            "line_user_id": line_user_id,
            "hanchan_id": {"$in": hanchan_ids},
        })
    else:
        user_hanchans = user_hanchan_repository.find({"line_user_id": line_user_id})

    total = len(user_hanchans)
    if total == 0:
        return jsonify({
            "total_hanchan": 0,
            "total_point": 0,
            "average_rank": 0,
            "rank_distribution": {"first": 0, "second": 0, "third": 0, "fourth": 0},
            "point_history": [],
        })

    total_point = sum(uh.point for uh in user_hanchans) / 1000
    avg_rank = sum(uh.rank for uh in user_hanchans) / total
    dist = {"first": 0, "second": 0, "third": 0, "fourth": 0}
    for uh in user_hanchans:
        key = ["first", "second", "third", "fourth"][uh.rank - 1]
        dist[key] += 1

    # ポイント推移(累積)
    sorted_uhs = sorted(user_hanchans, key=lambda x: x.created_at)
    history = []
    cumulative = 0
    for uh in sorted_uhs:
        cumulative += uh.point / 1000
        history.append({
            "date": uh.created_at.strftime("%m/%d"),
            "point": round(cumulative, 1),
        })

    return jsonify({
        "total_hanchan": total,
        "total_point": round(total_point, 1),
        "average_rank": round(avg_rank, 2),
        "rank_distribution": dist,
        "point_history": history,
    })
