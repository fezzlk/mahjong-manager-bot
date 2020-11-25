from enum import Enum

class Modes(Enum):
    wait = 'wait'

class UserService:

    def __init__(self, services):
        self.services = services
        self.modes = Modes
        self.users = {}

    def register(self):
        user_id = self.services.app_service.req_user_id
        self.users[user_id] = {}
        self.users[user_id]['mode'] = self.modes.wait
        self.users[user_id]['history'] = []