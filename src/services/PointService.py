from .interfaces.IPointService import IPointService
from typing import Tuple


class PointService(IPointService):

    def get_point_and_name_from_text(
        self,
        text: str,
    ) -> Tuple[str, str]:
        s = text.split()
        if len(s) >= 2:
            # ユーザー名に空白がある場合を考慮し、最後の要素をポイント、そのほかをユーザー名として判断する
            return s[-1], ' '.join(s[:-1])
        # fixme: ユーザー名「taro 100」の点数を削除しようとした場合に上の条件にひっかかる
        # 名前のみによるメッセージでの削除機能自体をやめるか
        elif len(s) == 1:
            return 'delete', s[0]
