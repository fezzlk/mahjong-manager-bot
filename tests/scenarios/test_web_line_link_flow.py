"""シナリオテスト: Web登録 → LINE連携リクエスト → 承認 のフロー

WebUser の作成から LINE アカウント連携の承認まで複数 Use Case を順に実行し
最終的な DB 状態を検証する。
"""

from application_models.page_contents import PageContents
from application_service import request_info_service
from domain_model.entities.user import User
from domain_model.entities.web_user import WebUser
from line_models.event import Event
from repositories import user_repository, web_user_repository
from use_cases.personal_line.request_link_line_web_use_case import (
    RequestLinkLineWebUseCase,
)
from use_cases.web.approve_link_line_user_use_case import ApproveLinkLineUserUseCase
from use_cases.web.view_approve_link_line_use_case import ViewApproveLinkLineUseCase

LINE_USER_ID = "U_scenario_weblink_001_abcdefgh"
WEB_USER_EMAIL = "scenario_link_test@example.com"


def test_web_line_link_flow(mocker):
    """Web LINE 連携フロー。

    1. WebUser を DB に登録
    2. LINE ユーザーがアカウント連携リクエストを送信
    3. WebUser に linked_line_user_id がセットされる
    4. ViewApproveLinkLineUseCase で連携情報が参照できる
    5. ApproveLinkLineUserUseCase で承認し is_approved_line_user = True になる
    """
    # url_for は Flask アプリコンテキスト外ではモックする
    mocker.patch(
        "use_cases.personal_line.request_link_line_web_use_case.url_for",
        return_value="/line/approve",
    )

    # === Step 1: WebUser 登録 ===
    web_user = web_user_repository.create(
        WebUser(
            user_code=WEB_USER_EMAIL,
            name="scenario_test_user",
            email=WEB_USER_EMAIL,
            linked_line_user_id=None,
            is_approved_line_user=False,
        ),
    )
    assert web_user._id is not None

    # === Step 2: LINE からアカウント連携リクエスト ===
    event = Event(
        type="message",
        source_type="user",
        user_id=LINE_USER_ID,
        message_type="text",
        text=f"アカウント連携 {WEB_USER_EMAIL}",
    )
    request_info_service.set_req_info(event)
    RequestLinkLineWebUseCase().execute()

    # === Step 3: WebUser に linked_line_user_id がセットされている ===
    updated = web_user_repository.find_by_id(web_user._id)
    assert updated.linked_line_user_id == LINE_USER_ID
    assert updated.is_approved_line_user is False  # まだ未承認

    # === Step 4: 管理者が承認画面を参照 (ViewApproveLinkLineUseCase) ===
    # LINE ユーザーも DB に登録しておく
    user_repository.create(
        User(
            line_user_id=LINE_USER_ID,
            line_user_name="scenario_line_user",
        ),
    )
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = updated
    result_pc = ViewApproveLinkLineUseCase().execute(page_contents)
    assert result_pc.page_title == "LINEアカウント連携"
    assert result_pc.line_user_name == "scenario_line_user"

    # === Step 5: 承認実行 (ApproveLinkLineUserUseCase) ===
    page_contents2 = PageContents(session={}, request=None)
    page_contents2.login_user = updated
    ApproveLinkLineUserUseCase().execute(page_contents2)

    approved = web_user_repository.find_by_id(web_user._id)
    assert approved.is_approved_line_user is True
    assert page_contents2.message == "LINEアカウント連携を承認しました。"
