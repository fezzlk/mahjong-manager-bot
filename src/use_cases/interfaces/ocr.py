from abc import ABC, abstractmethod


class IOcrUseCases(ABC):

    @abstractmethod
    def input_result_from_image(self):
        pass
