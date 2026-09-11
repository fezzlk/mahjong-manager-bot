from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from bson.objectid import ObjectId

from domain_model.entities.group_setting import EmbeddedGroupSettings


class GroupMode(Enum):
    wait = "wait"
    input = "input"
    sim = "sim"
    chip_input = "chip_input"
    chip_ok = "chip_ok"


@dataclass
class Group:
    line_group_id: str
    mode: str = GroupMode.wait.value
    # 「今テキスト入力を受け付けているMatch」を指す一時的なセッションポインタ。
    # 「どの対戦が進行中(open)か」の正本ではない(それはMatch.status、FEZ-66 Phase D)。
    # 複数対戦が同時にopenでありうるため、このポインタはそのうちの高々1つ(現在の
    # 入力対象)しか指さない。Mongo上のフィールド名は歴史的経緯によりactive_match_id
    # のまま(データマイグレーション不要にするための意図的な命名乖離、group_repository参照)。
    current_input_match_id: ObjectId = field(default=None)
    # _sim専用の使い捨てサンドボックスMatch。current_input_match_idとは独立に保持し、
    # 実系列の入力中データを_simが上書きしないようにする(FEZ-66 Phase C)。
    sim_match_id: ObjectId = field(default=None)
    settings: Optional[EmbeddedGroupSettings] = field(default=None)
    last_command: str = field(default=None)
    group_name: Optional[str] = field(default=None)
    group_picture_url: Optional[str] = field(default=None)
    last_command_at: Optional[datetime] = field(default=None)
    merged_into: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):  # noqa: D105
        if self.mode not in GroupMode._member_names_:
            raise ValueError(f"GroupMode の値({self.mode})が不適切です。")
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
