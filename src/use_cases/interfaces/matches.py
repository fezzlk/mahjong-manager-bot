from abc import ABC, abstractmethod


class IMatchesUseCases(ABC):

    @abstractmethod
    def drop_result_by_number(self, result_number: int):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def finish(self):
        pass

    @abstractmethod
    def reply(self):
        pass

    @abstractmethod
    def reply_sum_matches_by_ids(self, args: list):
        pass
