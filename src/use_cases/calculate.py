"""calculate"""

import json
from server import logger
from services import (
    app_service,
    user_service,
    reply_service,
    matches_service,
    room_service,
    config_service,
    hanchans_service,
    calculate_service,
)


class CalculateUseCases:
    """
    calculate points
    """

    def calculate(self, points=None, tobashita_player_id=None):
        """
        得点計算の準備および結果の格納
        """
        room_id = app_service.req_room_id
        # points の取得(デフォルトでは引数 points が採用される)
        # 引数に points がない場合、現在 active な result (current)のポイントを計算対象にする
        if points is None:
            current = hanchans_service.get_current(room_id)
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
        if (any(x < 0 for x in points.values())) & (tobashita_player_id is None):
            reply_service.add_tobi_menu([
                {'id': p_id, 'name': user_service.get_name_by_user_id(p_id), }
                for p_id in points.keys() if points[p_id] > 0
            ])
            return

        # config の取得(by target で撮っちゃって良い)
        # 計算の実行
        calculate_result = calculate_service.calculate(
            points=points,
            ranking_prize=[int(s) for s in config_service.get_by_key(room_id, '順位点').split(',')],
            tobi_prize=int(config_service.get_by_key(room_id, '飛び賞')),
            rounding_method=config_service.get_by_key(room_id, '端数計算方法'),
            tobashita_player_id=tobashita_player_id,
        )

        # その半荘の結果を更新
        hanchans_service.update_result(calculate_result)

        # 総合結果に半荘結果を追加
        matches_service.add_result()

        # 結果の表示
        hanchans_service.reply_current_result()

        # 一半荘の結果をアーカイブ
        hanchans_service.archive()

        # ルームを待機モードにする
        room_service.chmod(
            room_service.modes.wait
        )
