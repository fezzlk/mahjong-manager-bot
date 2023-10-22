from .Mentionee import Mentionee
class Mention:
    def __init__(
            self, 
            mention_ids=[], 
        ):
        self.mentionees = [Mentionee(user_id=user_id) for user_id in mention_ids]
