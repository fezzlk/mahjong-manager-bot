from domain_model.entities.group_setting import EmbeddedGroupSettings


def test_default_values_for_four_players():
    # 目的: デフォルト(4人麻雀)のranking_prize/starting_points/return_pointsを確認する
    settings = EmbeddedGroupSettings()

    assert settings.num_of_players == 4
    assert settings.ranking_prize == [20, 10, -10, -20]
    assert settings.starting_points == 25000
    assert settings.return_points == 30000


def test_default_values_for_three_players():
    # 目的: 3人麻雀のデフォルトranking_prize/starting_points/return_pointsを確認する
    settings = EmbeddedGroupSettings(num_of_players=3)

    assert settings.ranking_prize == [30, 0, -30]
    assert settings.starting_points == 35000
    assert settings.return_points == 40000


def test_switching_num_of_players_preserves_both_settings():
    # 目的: num_of_playersを切り替えても、もう一方の人数の設定値が失われないこと
    settings = EmbeddedGroupSettings(
        num_of_players=4,
        ranking_prize_4=[30, 10, -10, -30],
    )

    settings.num_of_players = 3
    assert settings.ranking_prize == [30, 0, -30]
    settings.ranking_prize = [15, 0, -15]
    assert settings.ranking_prize_3 == [15, 0, -15]

    settings.num_of_players = 4
    assert settings.ranking_prize == [30, 10, -10, -30]


def test_from_dict_migrates_legacy_single_ranking_prize_to_four_players():
    # 目的: 旧スキーマ(単一ranking_prizeキー)がranking_prize_4として引き継がれること
    settings = EmbeddedGroupSettings.from_dict({
        "ranking_prize": [30, 10, -10, -30],
        "num_of_players": 4,
    })

    assert settings.ranking_prize_4 == [30, 10, -10, -30]
    assert settings.ranking_prize_3 == [30, 0, -30]
    assert settings.ranking_prize == [30, 10, -10, -30]


def test_to_dict_round_trip():
    # 目的: to_dict()の内容でfrom_dict()した結果が元のインスタンスと一致すること
    settings = EmbeddedGroupSettings(
        num_of_players=3,
        ranking_prize_3=[15, 0, -15],
        starting_points_3=40000,
    )

    restored = EmbeddedGroupSettings.from_dict(settings.to_dict())

    assert restored.ranking_prize_3 == [15, 0, -15]
    assert restored.starting_points_3 == 40000
    assert restored.num_of_players == 3
