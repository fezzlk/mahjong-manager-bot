from xml.dom import NotFoundErr

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from use_cases.web.delete_configs_for_web_use_case import DeleteConfigsForWebUseCase
from use_cases.web.get_config_for_web_use_case import GetConfigForWebUseCase
from use_cases.web.get_configs_for_web_use_case import GetConfigsForWebUseCase
from use_cases.web.update_config_for_web_use_case import UpdateConfigForWebUseCase

config_blueprint = Blueprint(
    "config_blueprint",
    __name__,
    url_prefix="/config",
)


@config_blueprint.route("/")
def get_configs():
    data = GetConfigsForWebUseCase().execute()
    keys = ["_id", "rate", "ranking_prize", "chip_rate", "tobi_prize", "num_of_players", "rounding_method"]
    input_keys = ["rate", "ranking_prize", "chip_rate", "tobi_prize", "num_of_players", "rounding_method"]
    return render_template(
        "model.html",
        title="configs",
        submit_to="create_config",
        keys=keys,
        input_keys=input_keys,
        data=data,
    )


@config_blueprint.route("/<_id>")
def configs_detail(_id):
    data = GetConfigForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ["line_group_id", "rate", "ranking_prize", "chip_rate", "tobi_prize", "num_of_players", "rounding_method"]
    return render_template(
        "detail.html",
        title="configs",
        submit_to="update_config",
        input_keys=input_keys,
        init_data=data,
    )


@config_blueprint.route("/create", methods=["POST"])
def create_config():
    return redirect(url_for("config_blueprint.get_configs"))


@config_blueprint.route("/update", methods=["POST"])
def update_config():
    UpdateConfigForWebUseCase().execute()
    return redirect(url_for("config_blueprint.get_configs"))


@config_blueprint.route("/delete", methods=["POST"])
def delete_configs():
    target_id = request.args.get("target_id")
    DeleteConfigsForWebUseCase().execute([target_id])
    return redirect(url_for("config_blueprint.get_configs"))
