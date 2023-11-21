from dataclasses import dataclass


@dataclass()
class Postback:
    data: str

    def __init__(self, data=''):
        self.data = data
