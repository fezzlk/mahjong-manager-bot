"""point"""


class PointsService:
    """point service"""

    def __init__(self, services):
        self.services = services

    def reply(self):
        """reply"""

        room_id = self.services.app_service.req_room_id
        points = self.services.room_service.rooms[room_id]['points']
        if len(points) == 0:
            self.services.reply_service.add_text(
                '点数を入力してください。「@{ユーザー名} {点数}」でユーザーを指定して入力することもできます。')
            return
        result = [f'{user}: {point}' for user, point in points.items()]
        self.services.reply_service.add_text("\n".join(result))

    def add_by_text(self, text):
        room_id = self.services.app_service.req_room_id
        points = self.services.room_service.rooms[room_id]['points']
        profile = self.services.app_service.line_bot_api.get_profile(
            self.services.app_service.req_user_id)
        target_user = profile.display_name
        if text[0] == '@':
            point, target_user = self.get_point_with_target_user(text[1:])
            point = point.replace(',', '')
            if point == 'delete':
                self.drop(target_user)
                self.reply()
                if len(points) == 4:
                    self.services.calculate_service.calculate(points)
                return
        else:
            point = text.replace(',', '')
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if point.isdigit() == False:
            self.services.reply_service.add_text(
                '点数は整数で入力してください。全員分の点数入力を終えた場合は _calc と送信してください。（中断したい場合は _exit)')
            return

        if isMinus == True:
            point = '-' + point

        self.add(target_user, int(point))
        self.reply()
        if len(points) == 4:
            self.services.calculate_service.calculate(points)
        elif len(points) > 4:
            self.services.reply_service.add_text(
                '5人以上入力されています。@{ユーザー名} で不要な入力を消してください。')

    def get_point_with_target_user(self, text):
        s = text.split()
        if len(s) >= 2:
            return s[-1], ' '.join(s[:-1])
        elif len(s) == 1:
            return 'delete', s[0]

    def add(self, name, point):
        room_id = self.services.app_service.req_room_id
        points = self.services.room_service.rooms[room_id]['points']
        points[name] = point

    def drop(self, name):
        room_id = self.services.app_service.req_room_id
        points = self.services.room_service.rooms[room_id]['points']
        if name in points.keys():
            points.pop(name)

    def reset(self):
        room_id = self.services.app_service.req_room_id
        self.services.room_service.rooms[room_id]['points'] = {}
