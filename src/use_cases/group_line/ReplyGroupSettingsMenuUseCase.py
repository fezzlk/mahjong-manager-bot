from DomainService import (
    group_setting_service,
)
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.GroupSetting import ROUNDING_METHOD_LIST


class ReplyGroupSettingsMenuUseCase:

    def execute(self, body) -> None:
        settings = group_setting_service.find_or_create(request_info_service.req_line_group_id)

        if body == '':
            r = settings.ranking_prize

            s = ['[設定]']
            s.append(f'{settings.num_of_players}人麻雀')
            s.append(f'レート: 点{settings.rate}')
            s.append(f'順位点: 1着{r[0]}/2着{r[1]}/3着{r[2]}/4着{r[3]}')
            s.append(f'飛び賞: {settings.tobi_prize}点')
            s.append(f'チップ: 1枚{settings.tip_rate}点')
            s.append(f'計算方法: {ROUNDING_METHOD_LIST[settings.rounding_method]}')
            reply_service.add_message('\n'.join(s))
        reply_service.add_settings_menu(body)
