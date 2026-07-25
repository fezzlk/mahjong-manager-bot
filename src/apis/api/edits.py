from datetime import datetime

from bson.objectid import ObjectId
from flask import jsonify, make_response, request

from application_service import calculate_service, reply_service
from domain_model.entities.user_hanchan import UserHanchanResult
from domain_service import group_setting_service, hanchan_service
from mongo_client import audit_logs_collection
from repositories import (
    hanchan_repository,
    match_repository,
    user_hanchan_repository,
)

from . import api_blueprint
from ._auth import assert_group_member, require_web_user


def _recalc_sum_scores(match_id):
    hanchans = hanchan_repository.find({
        "match_id": match_id,
        "converted_scores": {"$ne": {}},
    })
    sum_scores = {}
    for h in hanchans:
        for uid, score in h.converted_scores.items():
            sum_scores[uid] = sum_scores.get(uid, 0) + score
    return sum_scores


def _write_audit_log(operator_id, action, target_id, before, after):
    audit_logs_collection.insert_one({
        "operator_line_user_id": operator_id,
        "action": action,
        "target_id": str(target_id),
        "before": before,
        "after": after,
        "created_at": datetime.now(),
    })


@api_blueprint.route("/hanchans/<hanchan_id>", methods=["DELETE"])
@require_web_user
def delete_hanchan(web_user, hanchan_id):
    try:
        hanchans = hanchan_repository.find({"_id": ObjectId(hanchan_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not hanchans:
        return make_response(jsonify({"error": "Not found"}), 404)
    hanchan = hanchans[0]

    err = assert_group_member(web_user, hanchan.line_group_id)
    if err:
        return err

    hanchan_repository.update({"_id": hanchan._id}, {"is_deleted": True})
    user_hanchan_repository.delete({"hanchan_id": hanchan._id})

    matches = match_repository.find({"_id": hanchan.match_id})
    if matches:
        sum_scores = _recalc_sum_scores(hanchan.match_id)
        match_repository.update({"_id": hanchan.match_id}, {"sum_scores": sum_scores})
        reply_service.push_a_message(
            to=hanchan.line_group_id,
            message="[Web] 半荘データが削除されました。",
        )

    _write_audit_log(
        web_user.linked_line_user_id,
        "delete_hanchan",
        hanchan._id,
        {"is_deleted": False},
        {"is_deleted": True},
    )
    return jsonify({"ok": True})


@api_blueprint.route("/hanchans/<hanchan_id>/scores", methods=["PUT"])
@require_web_user
def update_hanchan_scores(web_user, hanchan_id):
    try:
        hanchans = hanchan_repository.find({"_id": ObjectId(hanchan_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not hanchans:
        return make_response(jsonify({"error": "Not found"}), 404)
    hanchan = hanchans[0]

    err = assert_group_member(web_user, hanchan.line_group_id)
    if err:
        return err

    body = request.get_json(silent=True) or {}
    try:
        new_raw_scores = {k: int(v) for k, v in body.get("raw_scores", {}).items()}
    except (ValueError, TypeError):
        return make_response(jsonify({"error": "素点は整数で指定してください"}), 400)

    if len(new_raw_scores) != 4:
        return make_response(jsonify({"error": "4人分の素点が必要です"}), 400)
    total = sum(new_raw_scores.values())
    if not (100000 <= total <= 100099):
        return make_response(jsonify({"error": f"素点の合計が不正です: {total}"}), 400)
    if len(set(new_raw_scores.values())) != 4:
        return make_response(jsonify({"error": "同点は許可されていません"}), 400)

    setting = group_setting_service.find_or_create(hanchan.line_group_id)
    tobashita_id = None
    if any(v < 0 for v in new_raw_scores.values()):
        tobashita_id = max(
            (uid for uid, v in new_raw_scores.items() if v > 0),
            key=lambda uid: new_raw_scores[uid],
            default=None,
        )
    new_converted = calculate_service.run(
        points=new_raw_scores,
        ranking_prize=setting.ranking_prize,
        tobi_prize=setting.tobi_prize,
        rounding_method=setting.rounding_method,
        tobashita_player_id=tobashita_id,
    )

    sorted_items = sorted(new_raw_scores.items(), key=lambda x: x[1], reverse=True)
    new_results = [
        UserHanchanResult(line_user_id=uid, point=score, rank=i + 1)
        for i, (uid, score) in enumerate(sorted_items)
    ]

    before = {
        "raw_scores": hanchan.raw_scores,
        "converted_scores": hanchan.converted_scores,
    }
    hanchan_repository.update({"_id": hanchan._id}, {
        "raw_scores": new_raw_scores,
        "converted_scores": new_converted,
        "results": new_results,
    })

    for r in new_results:
        existing_uhs = user_hanchan_repository.find({
            "hanchan_id": hanchan._id,
            "line_user_id": r.line_user_id,
        })
        if existing_uhs:
            user_hanchan_repository.update(
                {"_id": existing_uhs[0]._id},
                {"point": new_converted[r.line_user_id], "rank": r.rank},
            )

    sum_scores = _recalc_sum_scores(hanchan.match_id)
    match_repository.update({"_id": hanchan.match_id}, {"sum_scores": sum_scores})

    reply_service.push_a_message(
        to=hanchan.line_group_id,
        message="[Web] 半荘データが修正されました。",
    )
    _write_audit_log(
        web_user.linked_line_user_id,
        "update_hanchan_scores",
        hanchan._id,
        before,
        {"raw_scores": new_raw_scores, "converted_scores": new_converted},
    )
    return jsonify({"ok": True})


@api_blueprint.route("/matches/<match_id>", methods=["DELETE"])
@require_web_user
def delete_match(web_user, match_id):
    try:
        matches = match_repository.find({"_id": ObjectId(match_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not matches:
        return make_response(jsonify({"error": "Not found"}), 404)
    match = matches[0]

    err = assert_group_member(web_user, match.line_group_id)
    if err:
        return err

    match_repository.update({"_id": match._id}, {"is_deleted": True})
    hanchan_service.disable_by_match_id(match._id)

    reply_service.push_a_message(
        to=match.line_group_id,
        message="[Web] 対戦データが削除されました。",
    )
    _write_audit_log(
        web_user.linked_line_user_id,
        "delete_match",
        match._id,
        {"is_deleted": False},
        {"is_deleted": True},
    )
    return jsonify({"ok": True})


@api_blueprint.route("/matches/<match_id>/chips", methods=["PUT"])
@require_web_user
def update_match_chips(web_user, match_id):
    try:
        matches = match_repository.find({"_id": ObjectId(match_id)})
    except Exception:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not matches:
        return make_response(jsonify({"error": "Not found"}), 404)
    match = matches[0]

    err = assert_group_member(web_user, match.line_group_id)
    if err:
        return err

    body = request.get_json(silent=True) or {}
    try:
        new_chip_scores = {k: int(v) for k, v in body.get("chip_scores", {}).items()}
    except (ValueError, TypeError):
        return make_response(jsonify({"error": "チップ数は整数で指定してください"}), 400)

    before = {"chip_scores": match.chip_scores}
    match_repository.update({"_id": match._id}, {"chip_scores": new_chip_scores})

    reply_service.push_a_message(
        to=match.line_group_id,
        message="[Web] チップデータが修正されました。",
    )
    _write_audit_log(
        web_user.linked_line_user_id,
        "update_chips",
        match._id,
        before,
        {"chip_scores": new_chip_scores},
    )
    return jsonify({"ok": True})
