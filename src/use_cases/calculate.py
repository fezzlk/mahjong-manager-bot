"""calculate"""

import json
from server import logger
from services import (
    user_service,
    reply_service,
    results_service,
    matches_service,
    room_service,
    config_service
)


class CalculateUseCases:
    """
    calculate points
    """

    def calculate(self, points=None, tobashita_player_id=None):
        """
        得点計算の準備および結果の格納
        """

        # points の取得(デフォルトでは引数 points が採用される)
        # 引数に points がない場合、現在 active な result (current)のポイントを計算対象にする
        if points is None:
            current = results_service.get_current()
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

        # 計算の実行
        calc_result = self.run_calculate(points, tobashita_player_id)

        # その半荘の結果を更新
        results_service.update_result(calc_result)

        # 総合結果に半荘結果を追加
        matches_service.add_result()

        # 結果の表示
        results_service.reply_current_result()

        # はんちゃん結果をアーカイブ
        results_service.archive()

        # ルームを待機モードにする
        room_service.chmod(
            room_service.modes.wait
        )

    def run_calculate(self, points, tobashita_player_id=None):
        """
        得点計算
        """

        # 準備
        sorted_points = sorted(
            points.items(), key=lambda x: x[1], reverse=True)
        sorted_prize = sorted(
            [int(s) for s in config_service.get_by_key(
                '順位点').split(',')],
            reverse=True,
        )
        tobi_prize = int(config_service.get_by_key('飛び賞'))
        # 計算方法合わせて点数調整用の padding を設定
        calculate_method = config_service.get_by_key('端数計算方法')
        padding = 0
        if calculate_method == '五捨六入':
            padding = 400
        elif calculate_method == '四捨五入':
            padding = 500
        elif calculate_method == '切り捨て':
            padding = 0
        elif calculate_method == '切り上げ':
            padding = 900

        # 素点計算
        result = {}
        tobasare_players = []
        isTobi = not(tobashita_player_id is None or
                     tobashita_player_id == '')
        # 2~4位
        for t in sorted_points[1:]:
            player = t[0]
            point = t[1]
            # 点数がマイナスの場合、飛ばされたプレイヤーリストに追加する
            if (point < 0):
                tobasare_players.append(player)

            # マイナス点の場合の端数処理を考慮するため、100000足して130(=(100000+30000)/1000)を引く
            result[player] = int((point + 10000 + padding) / 1000) - 130

        # 1位(他プレイヤーの点数合計×(-1))
        result[sorted_points[0][0]] = -1 * sum(result.values())

        # 順位点、飛び賞加算
        for i, t in enumerate(sorted_points):
            # 順位点
            result[t[0]] += sorted_prize[i]
            # 飛び賞
            if isTobi:
                if t[0] in tobasare_players:
                    result[t[0]] -= tobi_prize
                if t[0] == tobashita_player_id:
                    result[t[0]] += tobi_prize * len(tobasare_players)
                else:
                    logger.warning(
                        'tobashita_player_id is not matching'
                    )
        return result
