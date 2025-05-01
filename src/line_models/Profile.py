
# LINE messaging API に合わせるためフィールド名はキャメルケースにしている
class Profile:
    def __init__(
        self,
        display_name="",
        user_id="",
    ):
        self.display_name = display_name
        self.user_id = user_id
