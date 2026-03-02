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
from ._auth import assert_group_member, require_web_user


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
    err = assert_group_member(web_user, line_group_id)
    if err:
        return err

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
    """グループ統計(グラフ用データ)"""
    from bson.objectid import ObjectId  # noqa: PLC0415

    try:
        groups = group_repository.find({"_id": ObjectId(group_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not groups:
        return make_response(jsonify({"error": "Not found"}), 404)

    line_group_id = groups[0].line_group_id
    err = assert_group_member(web_user, line_group_id)
    if err:
        return err

    matches = match_repository.find(
        {"line_group_id": line_group_id},
        sort=[("created_at", 1)],
    )

    # 累積ポイント推移: line_user_id をキーに集計し、表示名は別途解決する
    cumulative: dict[str, float] = defaultdict(float)
    rank_dist: dict[str, dict] = defaultdict(lambda: {"first": 0, "second": 0, "third": 0, "fourth": 0})
    user_name_map: dict[str, str] = {}  # line_user_id -> display name
    point_history = []

    for match in matches:
        hanchans = hanchan_repository.find(
            {"match_id": match._id},
            sort=[("created_at", 1)],
        )
        for hanchan in hanchans:
            user_hanchans = user_hanchan_repository.find({"hanchan_id": hanchan._id})
            for uh in user_hanchans:
                uid = uh.line_user_id
                if uid not in user_name_map:
                    users = user_repository.find({"line_user_id": uid})
                    user_name_map[uid] = users[0].line_user_name if users else uid
                cumulative[uid] += uh.point / 1000
                rank_key = ["first", "second", "third", "fourth"][uh.rank - 1]
                rank_dist[uid][rank_key] += 1

            date_str = hanchan.created_at.strftime("%m/%d")
            entry: dict = {"date": date_str}
            # キーを表示名に変換してフロントエンドへ渡す
            entry.update({user_name_map[uid]: round(v, 1) for uid, v in cumulative.items()})
            point_history.append(entry)

    rank_distribution = [
        {"user_name": user_name_map[uid], **dist}
        for uid, dist in rank_dist.items()
    ]

    return jsonify({
        "point_history": point_history,
        "rank_distribution": rank_distribution,
    })
