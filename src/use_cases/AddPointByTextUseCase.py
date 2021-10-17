from services import (
    request_info_service,
    reply_service,
    points_service,
    user_service,
    hanchan_service,
    calculate_service,
    config_service,
    match_service,
    room_service,
    message_service,
)
from domains.Room import RoomMode


class AddPointByTextUseCase:

    def execute(self, text):
        line_room_id = request_info_service.req_line_room_id

        if text[0] == '@':
            point, target_user = points_service.get_point_and_name_from_text(
                text[1:]
            )
            target_line_user_id = user_service.get_user_id_by_name(
                target_user
            )

            if point == 'delete':
                points = hanchan_service.drop_raw_score(
                    line_room_id,
                    target_line_user_id,
                )

                res = [
                    f'{user_service.get_name_by_line_user_id(user_id)}: {point}'
                    for user_id, point in points.items()
                ]

                reply_service.add_message("\n".join(res))

                return
        else:
            target_line_user_id = request_info_service.req_line_user_id
            point = text

        point = point.replace(',', '')

        # 入力した点数のバリデート（hack: '-' を含む場合数値として判断できないため一旦エスケープ）
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if not point.isdigit():
            reply_service.add_message(
                '点数は整数で入力してください。')
            return None

        if isMinus:
            point = '-' + point

        points = hanchan_service.create_raw_score(
            line_room_id=line_room_id,
            line_user_id=target_line_user_id,
            raw_score=int(point),
        )

        res = [
            f'{user_service.get_name_by_line_user_id(user_id)}: {point}'
            for user_id, point in points.items()
        ]

        reply_service.add_message("\n".join(res))

        if len(points) == 4:
            """
            得点計算の準備および結果の格納
            """

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

            # 飛び賞が発生した場合、飛び賞を受け取るプレイヤーを指定するメニューを返す
            if any(x < 0 for x in points.values()):
                reply_service.add_tobi_menu([
                    {'id': p_id, 'name': user_service.get_name_by_line_user_id(p_id), }
                    for p_id in points.keys() if points[p_id] > 0
                ])
                return

            # config の取得(by target で撮っちゃって良い)
            # 計算の実行
            calculate_result = calculate_service.run_calculate(
                points=points,
                ranking_prize=[
                    int(s) for s in config_service.get_value_by_key(line_room_id, '順位点').split(',')
                ],
                rounding_method=config_service.get_value_by_key(line_room_id, '端数計算方法'),
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
                '5人以上入力されています。@{ユーザー名} で不要な入力を消してください。'
            )

        return
