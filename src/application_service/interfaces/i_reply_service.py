from abc import ABCMeta, abstractmethod
from typing import Dict, List

from linebot.v3.webhooks import Event

from domain_model.entities.user import User


class IReplyService(metaclass=ABCMeta):

    @abstractmethod
    def add_message(
        self,
        text: str,
    ) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def add_submit_results_by_ocr_menu(self, results: Dict[str, int]) -> None:
        pass

    @abstractmethod
    def add_tobi_menu(self, player_id_and_names: List[Dict[str, str]]) -> None:
        pass

    @abstractmethod
    def add_settings_menu(self, key: str = "") -> None:
        pass

    @abstractmethod
    def add_others_menu(self) -> None:
        pass

    @abstractmethod
    def add_start_menu(self) -> None:
        pass

    @abstractmethod
    def add_confirm_finish_menu(self) -> None:
        pass

    @abstractmethod
    def add_image(self, image_url: str) -> None:
        pass

    @abstractmethod
    def reply(self, event: Event) -> None:
        pass

    @abstractmethod
    def create_and_reply_file_upload_error(self, title: str, sender: str) -> None:
        pass

    @abstractmethod
    def add_history_target_quick_reply(self) -> None:
        pass

    @abstractmethod
    def add_history_period_quick_reply(self) -> None:
        pass

    @abstractmethod
    def add_history_user_select_carousel(
        self, members: List[User], selected_ids: List[str],
    ) -> None:
        pass
