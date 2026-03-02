from flask import jsonify, make_response

from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_hanchan_repository,
    user_repository,
)
from . import api_blueprint
from ._auth import require_web_user


@api_blueprint.route("/groups/<group_id>/matches", methods=["GET"])
@require_web_user
def get_matches(web_user, group_id):
    """グループ内の試合一覧"""
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        groups = group_repository.find({"_id": ObjectId(group_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not groups:
        return make_response(jsonify({"error": "Not found"}), 404)

    line_group_id = groups[0].line_group_id
    matches = match_repository.find(
        {"line_group_id": line_group_id},
        sort=[("created_at", -1)],
    )

    result = []
    for m in matches:
        hanchans = hanchan_repository.find(
            {"match_id": m._id},
        )
        result.append({
            "id": str(m._id),
            "group_id": group_id,
            "date": m.created_at.isoformat(),
            "hanchan_count": len(hanchans),
            "is_deleted": m.is_deleted,
        })

    return jsonify(result)


@api_blueprint.route("/matches/<match_id>", methods=["GET"])
@require_web_user
def get_match(web_user, match_id):
    """試合詳細（半荘一覧含む）"""
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        matches = match_repository.find({"_id": ObjectId(match_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not matches:
        return make_response(jsonify({"error": "Not found"}), 404)

    m = matches[0]
    hanchans = hanchan_repository.find(
        {"match_id": m._id},
        sort=[("created_at", 1)],
    )

    hanchan_list = []
    for h in hanchans:
        user_hanchans = user_hanchan_repository.find({"hanchan_id": h._id})
        scores = []
        for uh in user_hanchans:
            users = user_repository.find({"line_user_id": uh.line_user_id})
            user_name = users[0].line_user_name if users else uh.line_user_id
            raw_score = h.raw_scores.get(uh.line_user_id, 0)
            scores.append({
                "user_id": uh.line_user_id,
                "user_name": user_name,
                "score": raw_score,
                "rank": uh.rank,
                "point": uh.point / 1000,
            })

        hanchan_list.append({
            "id": str(h._id),
            "match_id": match_id,
            "date": h.created_at.isoformat(),
            "scores": sorted(scores, key=lambda x: x["rank"]),
        })

    # グループ ID 取得
    groups = group_repository.find({"line_group_id": m.line_group_id})
    group_id = str(groups[0]._id) if groups else None

    return jsonify({
        "id": str(m._id),
        "group_id": group_id,
        "date": m.created_at.isoformat(),
        "hanchan_count": len(hanchans),
        "is_deleted": m.is_deleted,
        "hanchans": hanchan_list,
    })
