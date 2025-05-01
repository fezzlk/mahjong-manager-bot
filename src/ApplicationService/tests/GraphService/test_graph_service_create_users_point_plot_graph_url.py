import matplotlib.pyplot as plt

import env_var
from ApplicationService import graph_service


def test_execute(mocker):
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
    )

    line_id_name_dict = {
        "U0123456789abcdefghijklmnopqrstu1": "test_user1",
        "U0123456789abcdefghijklmnopqrstu2": "test_user2",
    }
    plot_dict = {
        "U0123456789abcdefghijklmnopqrstu1": [0, 1, 2],
        "U0123456789abcdefghijklmnopqrstu2": [0, 2, 4],
    }

    # Act
    image_url, err_message = graph_service.create_users_point_plot_graph_url(
        line_id_name_dict, plot_dict, "/image_path",
    )

    # Assert
    assert image_url == f"{env_var.SERVER_URL}uploads/image_path"
    assert err_message is None


def test_execute_fail_savefig(mocker):
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
        side_effect=FileNotFoundError(),
    )

    line_id_name_dict = {
        "U0123456789abcdefghijklmnopqrstu1": "test_user1",
        "U0123456789abcdefghijklmnopqrstu2": "test_user2",
    }
    plot_dict = {
        "U0123456789abcdefghijklmnopqrstu1": [0, 1, 2],
        "U0123456789abcdefghijklmnopqrstu2": [0, 2, 4],
    }

    # Act
    image_url, err_message = graph_service.create_users_point_plot_graph_url(
        line_id_name_dict, plot_dict, "/image_path",
    )

    # Assert
    assert image_url is None
    assert err_message == "対戦履歴の画像アップロードに失敗しました"
