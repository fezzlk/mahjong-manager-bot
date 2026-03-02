from flask import jsonify, make_response

from repositories import user_repository, web_user_repository
from . import api_blueprint
from ._auth import require_web_user


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
    from repositories import user_hanchan_repository, hanchan_repository  # noqa: PLC0415

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
