from collections import defaultdict

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


@api_blueprint.route("/groups/<group_id>/ranking", methods=["GET"])
@require_web_user
def get_ranking(web_user, group_id):
    """グループ内ランキング"""
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        groups = group_repository.find({"_id": ObjectId(group_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not groups:
        return make_response(jsonify({"error": "Not found"}), 404)

    line_group_id = groups[0].line_group_id
    matches = match_repository.find({"line_group_id": line_group_id})

    # 全半荘の user_hanchan を収集
    stats = defaultdict(lambda: {
        "total_point": 0,
        "hanchan_count": 0,
        "rank_sum": 0,
        "first": 0, "second": 0, "third": 0, "fourth": 0,
    })

    for match in matches:
        hanchans = hanchan_repository.find({"match_id": match._id})
        for hanchan in hanchans:
            user_hanchans = user_hanchan_repository.find({"hanchan_id": hanchan._id})
            for uh in user_hanchans:
                s = stats[uh.line_user_id]
                s["total_point"] += uh.point
                s["hanchan_count"] += 1
                s["rank_sum"] += uh.rank
                rank_key = ["first", "second", "third", "fourth"][uh.rank - 1]
                s[rank_key] += 1

    if not stats:
        return jsonify([])

    # ユーザー名解決
    ranking = []
    for line_user_id, s in stats.items():
        users = user_repository.find({"line_user_id": line_user_id})
        user_name = users[0].line_user_name if users else line_user_id
        avg_rank = s["rank_sum"] / s["hanchan_count"] if s["hanchan_count"] > 0 else 0
        ranking.append({
            "user_id": line_user_id,
            "user_name": user_name,
            "total_point": round(s["total_point"] / 1000, 1),
            "hanchan_count": s["hanchan_count"],
            "average_rank": round(avg_rank, 2),
            "first_count": s["first"],
            "second_count": s["second"],
            "third_count": s["third"],
            "fourth_count": s["fourth"],
        })

    ranking.sort(key=lambda x: x["total_point"], reverse=True)
    for i, entry in enumerate(ranking):
        entry["rank"] = i + 1

    return jsonify(ranking)


@api_blueprint.route("/groups/<group_id>/stats", methods=["GET"])
@require_web_user
def get_group_stats(web_user, group_id):
    """グループ統計（グラフ用データ）"""
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
        sort=[("created_at", 1)],
    )

    # 累積ポイント推移: {date_str: {user_name: cumulative_pt}}
    cumulative = defaultdict(float)
    point_history = []
    rank_dist = defaultdict(lambda: {"first": 0, "second": 0, "third": 0, "fourth": 0})

    for match in matches:
        hanchans = hanchan_repository.find(
            {"match_id": match._id},
            sort=[("created_at", 1)],
        )
        for hanchan in hanchans:
            user_hanchans = user_hanchan_repository.find({"hanchan_id": hanchan._id})
            for uh in user_hanchans:
                users = user_repository.find({"line_user_id": uh.line_user_id})
                user_name = users[0].line_user_name if users else uh.line_user_id
                cumulative[user_name] += uh.point / 1000
                rank_key = ["first", "second", "third", "fourth"][uh.rank - 1]
                rank_dist[user_name][rank_key] += 1

            date_str = hanchan.created_at.strftime("%m/%d")
            entry = {"date": date_str}
            entry.update({k: round(v, 1) for k, v in cumulative.items()})
            point_history.append(entry)

    rank_distribution = [
        {"user_name": name, **dist}
        for name, dist in rank_dist.items()
    ]

    return jsonify({
        "point_history": point_history,
        "rank_distribution": rank_distribution,
    })
