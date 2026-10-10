from .mentionee import Mentionee


class Mention:
    def __init__(
        self,
        mention_ids=[],
        mention_self=False,
    ):
        self.mentionees = [Mentionee(user_id=user_id) for user_id in mention_ids]
        if mention_self:
            self.mentionees.append(Mentionee(user_id="Ubot0000000000000000000000000000", is_self=True))
