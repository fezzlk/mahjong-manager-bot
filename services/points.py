class PointsService:

    def __init__(self, app_service, reply_service, config_service):
        self.app_service = app_service
        self.reply_service = reply_service
        self.config_service = config_service
        self.line_bot_api = self.reply_service.line_bot_api
        self.points = {}

    def reply(self):
        if len(self.points) == 0:
            self.reply_service.add('点数を入力してください。「@{ユーザー名} {点数}」でユーザーを指定して入力することもできます。')
            return
        result = [f'{user}: {point}' for user, point in self.points.items()]
        self.reply_service.add("\n".join(result))

    def add_by_text(self, text):
        profile = self.line_bot_api.get_profile(self.app_service.req_user_id)
        target_user = profile.display_name
        if text[0] == '@':
            point, target_user = self.get_point_with_target_user(text[1:])
            point = point.replace(',', '')
            if point == 'delete':
                self.drop(target_user)
                self.reply()
                return
        else:
            point = text.replace(',', '')
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if point.isdigit() == False:
            self.reply_service.add('点数は整数で入力してください。全員分の点数入力を終えた場合は @CALC と送信してください。（中断したい場合は @EXIT)')
            return

        if isMinus == True:
            point = '-' + point
        
        self.add(target_user, int(point))
        self.reply()

    def get_point_with_target_user(self, text):
        s = text.split()
        if len(s) >= 2:
            return s[-1], ' '.join(s[:-1])
        elif len(s) == 1:
            return 'delete', s[0]

    def add(self, name, point):
        self.points[name] = point

    def drop(self, name):
        if name in self.points.keys():
            self.points.pop(name)

    def reset(self):
        self.points = {}
