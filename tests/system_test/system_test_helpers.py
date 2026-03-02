"""システムテスト共通ヘルパー関数"""


def make_line_webhook_payload(events: list) -> dict:
    """LINE Webhook の JSON ペイロードを生成するヘルパー"""
    return {
        "destination": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "events": events,
    }


def make_group_text_event(group_id: str, user_id: str, text: str) -> dict:
    """グループチャットのテキストメッセージイベントを生成する"""
    return {
        "type": "message",
        "message": {
            "type": "text",
            "id": "test_message_id_001",
            "text": text,
        },
        "source": {
            "type": "group",
            "groupId": group_id,
            "userId": user_id,
        },
        "replyToken": "test_reply_token_001",
        "timestamp": 1625000000000,
        "mode": "active",
    }


def make_personal_text_event(user_id: str, text: str) -> dict:
    """個人チャットのテキストメッセージイベントを生成する"""
    return {
        "type": "message",
        "message": {
            "type": "text",
            "id": "test_message_id_002",
            "text": text,
        },
        "source": {
            "type": "user",
            "userId": user_id,
        },
        "replyToken": "test_reply_token_002",
        "timestamp": 1625000000000,
        "mode": "active",
    }
