from services import (
    request_info_service,
    reply_service,
    user_service,
    hanchan_service,
    message_service,
    match_service,
    config_service,
    room_service,
)
from domains.Room import RoomMode


class AddHanchanByPointsTextUseCase:

    def execute(self, text) -> None:
        rows = [r for r in text.split('\n') if ':' in r]
        points = {}
        for r in rows:
            col = r.split(':')
            points[
                user_service.get_line_user_id_by_name(col[0])
            ] = int(col[1])

        line_room_id = request_info_service.req_line_room_id
        current_match = match_service.get_or_add_current(line_room_id)
        hanchan_service.create(points, line_room_id, current_match)

        if len(points) == 4:
            # 得点計算の準備および結果の格納

            # 計算可能な points かチェック
            # 4人分の点数がない、または超えている場合中断する
            if len(points) != 4:
                reply_service.add_message(
                    '四人分の点数を入力してください。点数を取り消したい場合は @[ユーザー名] と送ってください。'
                )
                return

            # 点数合計が 100000~100099 の範囲になければ中断する
            if int(sum(points.values()) / 100) != 1000:
                reply_service.add_message(
                    f'点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。'
                )
                return

            # 点数が全て異なっているかチェックし、同点があったら中断する
            if len(set(points.values())) != 4:
                reply_service.add_message(
                    '同点のユーザーがいます。上家が1点でも高くなるよう修正してください。'
                )
                return

            # 飛び賞が発生した場合、飛び賞を受け取るプレイヤーを指定するメニューを返す
            if any(x < 0 for x in points.values()):
                reply_service.add_tobi_menu([
                    {'id': p_id, 'name': user_service.get_name_by_line_user_id(p_id), }
                    for p_id in points.keys() if points[p_id] > 0
                ])
                return

            # config の取得
            ranking_prize = config_service.get_value_by_key(line_room_id, '順位点')
            rounding_method = config_service.get_value_by_key(line_room_id, '端数計算方法')

            # 計算の実行
            calculate_result = hanchan_service.run_calculate(
                points=points,
                ranking_prize=[
                    int(s) for s in ranking_prize.split(',')
                ],
                rounding_method=rounding_method,
            )

            # その半荘の結果を更新
            current_hanchan = hanchan_service.update_converted_score(line_room_id, calculate_result)

            # 総合結果に半荘結果を追加
            current_match = match_service.add_hanchan_id(line_room_id, current_hanchan._id)

            # 結果の表示
            converted_scores = current_hanchan.converted_scores
            hanchans = hanchan_service.find_by_ids(
                current_match.hanchan_ids,
            )
            sum_hanchans = {}
            for r in hanchans:
                converted_scores = r.converted_scores
                for user_id, converted_score in converted_scores.items():
                    if user_id not in sum_hanchans.keys():
                        sum_hanchans[user_id] = 0
                    sum_hanchans[user_id] += converted_score

            reply_service.add_message(
                '一半荘お疲れ様でした。結果を表示します。'
            )

            score_text_list = []
            for r in sorted(
                converted_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                name = user_service.get_name_by_line_user_id(r[0])
                score = ("+" if r[1] > 0 else "") + str(r[1])
                sum_score = ("+" if sum_hanchans[r[0]] > 0 else "") + str(sum_hanchans[r[0]])
                score_text_list.append(
                    f'{name}: {score} ({sum_score})'
                )
            reply_service.add_message(
                '\n'.join(score_text_list)
            )

            reply_service.add_message(
                message_service.get_finish_hanchan_message()
            )

            # 一半荘の結果をアーカイブ
            hanchan_service.archive(line_room_id)

            # ルームを待機モードにする
            room_service.chmod(line_room_id, RoomMode.wait)

            reply_service.add_message(
                '始める時は「_start」と入力してください。'
            )

        elif len(points) > 4:
            reply_service.add_message(
                '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
            )

        return