"""point"""

import json


class PointsService:
    """point service"""

    def __init__(self, services):
        self.services = services

    def reply(self, result=None):
        """reply"""

        if result is None:
            result = self.services.hanchans_service.get_current()
        raw_scores = json.loads(result.raw_scores)
        if len(raw_scores) == 0:
            self.services.reply_service.add_message(
                '点数を入力してください。「@{ユーザー名} {点数}」でユーザーを指定して入力することもできます。')
            return
        res = [f'{self.services.user_service.get_name_by_user_id(user_id)}: {point}' for user_id, point in points.items()]
        self.services.reply_service.add_message("\n".join(res))

    def add_by_text(self, text):
        result = self.services.hanchans_service.get_current()
        if text[0] == '@':
            point, target_user = self.get_point_with_target_user(text[1:])
            target_user_id = self.services.user_service.get_user_id_by_name(
                target_user
            )
            point = point.replace(',', '')
            if point == 'delete':
                points = self.services.hanchans_service.drop_point(
                    target_user_id)
                self.reply()
                if len(points) == 4:
                    self.services.calculate_service.calculate(points)
                return
        else:
            target_user_id = self.services.app_service.req_user_id
            point = text.replace(',', '')
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if point.isdigit() == False:
            self.services.reply_service.add_message(
                '点数は整数で入力してください。全員分の点数入力を終えた場合は _calc と送信してください。（中断したい場合は _exit)')
            return

        if isMinus == True:
            point = '-' + point

        points = self.services.hanchans_service.add_point(
            target_user_id,
            int(point),
        )
        self.reply()

        if len(points) == 4:
            self.services.calculate_service.calculate(points)
        elif len(points) > 4:
            self.services.reply_service.add_message(
                '5人以上入力されています。@{ユーザー名} で不要な入力を消してください。')

    def get_point_with_target_user(self, text):
        s = text.split()
        if len(s) >= 2:
            return s[-1], ' '.join(s[:-1])
        elif len(s) == 1:
            return 'delete', s[0]

    def add_by_ocr(self):
        results = self.services.ocr_service.get_points()
        if results is None:
            return

        res_message = "\n".join([f'{user}: {(point//100)*100}' for user, point in results.items()])
        self.services.reply_service.add_message(res_message)
        self.services.reply_service.add_submit_results_by_ocr_menu(results)
