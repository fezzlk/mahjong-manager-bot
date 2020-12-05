"""user"""

from enum import Enum
from models import Users


class Modes(Enum):
    """mode"""

    wait = 'wait'


class UserService:
    """user service"""

    def __init__(self, services):
        self.services = services
        self.modes = Modes
        self.users = {}

    def register(self, profile):
        """register"""
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == profile.user_id).all()
        if len(target) >= 1:
            return
        user = Users(name=profile.display_name,
                     user_id=profile.user_id,
                     mode=self.modes.wait.value,
                     )
        self.services.app_service.db.session.add(user)
        self.services.app_service.db.session.commit()

        # user_id = self.services.app_service.req_user_id
        # self.users[user_id] = {}
        # self.users[user_id]['mode'] = self.modes.wait
        # self.users[user_id]['history'] = []
