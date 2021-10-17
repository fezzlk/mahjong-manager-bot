"""calculate"""

import json
from server import logger
from services import (
    request_info_service,
    user_service,
    reply_service,
    match_service,
    room_service,
    config_service,
    hanchan_service,
    calculate_service,
    message_service,
)


class CalculateUseCases:
    """
    calculate points
    """

    def calculate(self, points=None, tobashita_player_id=None):
        """
        得点計算の準備および結果の格納
        """
        room_id = request_info_service.req_line_room_id
        # points の取得(デフォルトでは引数 points が採用される)
        # 引数に points がない場合、現在 active な result (current)のポイントを計算対象にする
        if points is None:
            current = hanchan_service.get_current(room_id)
            if current is None:
                logger.error(
                    'current points is not found.'
                )
                return
            points = json.loads(current.points)

        # 計算可能な points かチェック
        # 4人分の点数がない、または超えている場合中断する
        if len(points) != 4:
            reply_service.add_message(
                '四人分の点数を入力してください。点数を取り消したい場合は @{ユーザー名} と送ってください。')
            return
        # 点数合計が 100000~100099 の範囲になければ中断する
        if int(sum(points.values()) / 100) != 1000:
            reply_service.add_message(
                f'点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。')
            return
        # 点数が全て異なっているかチェックし、同点があったら中断する
        if len(set(points.values())) != 4:
            reply_service.add_message(
                '同点のユーザーがいます。上家が1点でも高くなるよう修正してください。')
            return

        # 飛び賞が発生し、飛ばしたプレイヤーが未指定の場合、飛び賞を受け取るプレイヤーを指定するメニューを返す
        if (any(x < 0 for x in points.values())) & (
                tobashita_player_id is None):
            reply_service.add_tobi_menu([
                {'id': p_id, 'name': user_service.get_name_by_line_user_id(p_id), }
                for p_id in points.keys() if points[p_id] > 0
            ])
            return

        # config の取得(by target で撮っちゃって良い)
        # 計算の実行
        calculate_result = calculate_service.calculate(
            points=points, ranking_prize=[
                int(s) for s in config_service.get_value_by_key(
                    room_id, '順位点').split(',')], tobi_prize=int(
                config_service.get_value_by_key(
                    room_id, '飛び賞')), rounding_method=config_service.get_value_by_key(
                        room_id, '端数計算方法'), tobashita_player_id=tobashita_player_id, )

        room_id = request_info_service.req_line_room_id

        # その半荘の結果を更新
        hanchan_service.update_converted_score(room_id, calculate_result)

        # 総合結果に半荘結果を追加
        current_result = hanchan_service.get_current(room_id)
        match_service.add_result(room_id, current_result.id)

        # 結果の表示
        hanchan = hanchan_service.get_current(room_id)
        converted_scores = json.loads(hanchan.converted_scores)
        current_match = match_service.get_current()
        hanchans = hanchan_service.find_by_ids(
            json.loads(current_match.result_ids)
        )
        sum_hanchans = {}
        for r in hanchans:
            converted_scores = json.loads(r.converted_scores)
            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score

        reply_service.add_message(
            '一半荘お疲れ様でした。結果を表示します。'
        )
        reply_service.add_message(
            '\n'.join([
                f'{user_service.get_name_by_line_user_id(r[0])}: \
                {"+" if r[1] > 0 else ""}{r[1]} \
                ({"+" if sum_hanchans[r[0]] > 0 else ""}{sum_hanchans[r[0]]})'
                for r in sorted(
                    converted_scores.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )

        reply_service.add_message(
            message_service.get_hanchan_message()
        )

        # 一半荘の結果をアーカイブ
        hanchan_service.archive(room_id)

        # ルームを待機モードにする
        room_service.chmod(room_id, room_service.modes.wait)

        reply_service.add_message(
            '始める時は「_start」と入力してください。')
        return
