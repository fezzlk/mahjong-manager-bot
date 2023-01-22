from dataclasses import dataclass
from typing import Dict, List

DEFAULT_CONFIGS = {
    'レート': '点3',
    '順位点': ','.join(['20', '10', '-10', '-20']),
    '飛び賞': '10',
    'チップ': '0',
    '人数': '4',
    '端数計算方法': '3万点以下切り上げ/以上切り捨て',
}

GROUP_SETTING_DICT: Dict[str, List[str]] = {
    'レート': ['点1', '点2', '点3', '点4', '点5', '点10'],
    '順位点': [
        ','.join(['20', '10', '-10', '-20']),
        ','.join(['30', '10', '-10', '-30']),
    ],
    '飛び賞': ['0', '10', '20', '30'],
    'チップ': ['0', '30'],
    '人数': ['3', '4'],
    '端数計算方法': [
        '3万点以下切り上げ/以上切り捨て',
        '五捨六入',
        '四捨五入',
        '切り捨て',
        '切り上げ',
    ],
}


@dataclass()
class Config:
    _id: int
    target_id: str
    key: str
    value: str

    def __init__(
        self,
        target_id: str,
        key: str,
        value: str,
        _id=None,
    ):

        if key not in GROUP_SETTING_DICT.keys():
            raise ValueError(f'設定キー "{key}" が不適切です。')

        if value not in GROUP_SETTING_DICT[key]:
            raise ValueError(f'設定キー "{key}" に対して設定値 "{value}" が不適切です。')

        self._id = _id
        self.target_id = target_id
        self.key = key
        self.value = value
