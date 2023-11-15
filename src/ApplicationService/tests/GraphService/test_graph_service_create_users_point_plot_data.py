from use_cases.group_line.CreateMatchDetailGraphUseCase import CreateMatchDetailGraphUseCase
import matplotlib.pyplot as plt
import env_var
from ApplicationService import graph_service
from DomainModel.entities.Hanchan import Hanchan


dummy_archived_hanchans = [
    Hanchan(
        line_group_id='dummy_group',
        raw_scores={
            'U0123456789abcdefghijklmnopqrstu1': 40000,
            'U0123456789abcdefghijklmnopqrstu2': 30000,
            'U0123456789abcdefghijklmnopqrstu3': 20000,
            'U0123456789abcdefghijklmnopqrstu4': 10000,
        },
        converted_scores={
            'U0123456789abcdefghijklmnopqrstu1': 50,
            'U0123456789abcdefghijklmnopqrstu2': 10,
            'U0123456789abcdefghijklmnopqrstu3': -20,
            'U0123456789abcdefghijklmnopqrstu4': -40,
        },
        match_id=1,
        status=2,
        _id=1,
    ),
    Hanchan(
        line_group_id='dummy_group',
        raw_scores={
            'U0123456789abcdefghijklmnopqrstu1': 40000,
            'U0123456789abcdefghijklmnopqrstu2': 30000,
            'U0123456789abcdefghijklmnopqrstu3': 20000,
            'U0123456789abcdefghijklmnopqrstu4': 10000,
        },
        converted_scores={
            'U0123456789abcdefghijklmnopqrstu1': 50,
            'U0123456789abcdefghijklmnopqrstu2': 10,
            'U0123456789abcdefghijklmnopqrstu3': -20,
            'U0123456789abcdefghijklmnopqrstu5': -40,
        },
        match_id=1,
        status=2,
        _id=2,
    ),
]


def test_execute():
    # Arrange
    expected_line_id_list = {
        "U0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu2",
        "U0123456789abcdefghijklmnopqrstu3",
        "U0123456789abcdefghijklmnopqrstu4",
        "U0123456789abcdefghijklmnopqrstu5",
    }
    expected_plot_dict = {
        "U0123456789abcdefghijklmnopqrstu1": [0, 50, 100],
        "U0123456789abcdefghijklmnopqrstu2": [0, 10, 20],
        "U0123456789abcdefghijklmnopqrstu3": [0, -20, -40],
        "U0123456789abcdefghijklmnopqrstu4": [0, -40, -40],
        "U0123456789abcdefghijklmnopqrstu5": [0, 0, -40],
    }

    # Act
    line_id_list, plot_dict = graph_service.create_users_point_plot_data(
        dummy_archived_hanchans
    )

    # Assert
    assert len(line_id_list) == len(expected_line_id_list)
    for line_id in line_id_list:
        assert line_id in expected_line_id_list
    assert len(plot_dict) == len(expected_plot_dict)
    for line_id in plot_dict:
        plot_dict[line_id] == expected_plot_dict[line_id]
        