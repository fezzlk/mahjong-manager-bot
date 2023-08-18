from flask import (
    Blueprint,
    abort,
    request,
    render_template,
    url_for,
    redirect,
    session,
    send_from_directory,
)
from ApplicationModels.PageContents import PageContents
from use_cases.CreateDummyUseCase import CreateDummyUseCase

from linebot import WebhookHandler, exceptions
import env_var

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
views_blueprint = Blueprint('views_blueprint', __name__, url_prefix='/')


@views_blueprint.route('/')
def index():
    page_contents = PageContents(session, request)
    if request.args.get('message') is not None:
        page_contents.message = request.args.get('message')
    return render_template('index.html', page_contents=page_contents)


@views_blueprint.route("/callback", methods=['POST'])
def callback():
    """ Endpoint for LINE messaging API """

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'


@views_blueprint.route('/uploads/<path:filename>')
def download_file(filename: str):
    return send_from_directory(
        "uploads/",
        filename,
        as_attachment=True
    )


@views_blueprint.route('/login', methods=['GET'])
def view_login():
    page_contents = PageContents(session, request)
    return render_template(
        'login.html',
        page_contents=page_contents,
    )


@views_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views_blueprint.view_login'))


@views_blueprint.route('/create_dummy', methods=['POST'])
def create_dummy():
    CreateDummyUseCase().execute()
    return 'Done'

@views_blueprint.route('/migrate', methods=['POST'])
def migrate():
    from typing import Dict
    from repositories import (
        match_repository
    )
    from DomainService import (
        hanchan_service,
        match_service,
    )
    matches = match_repository.find()
    for active_match in matches:
        hanchans = hanchan_service.find_all_by_match_id(active_match._id)

        sum_scores: Dict[str, int] = {}
        for h in hanchans:
            for line_user_id, converted_score in h.converted_scores.items():
                if line_user_id not in sum_scores.keys():
                    sum_scores[line_user_id] = 0
                sum_scores[line_user_id] += converted_score


        rate = 30
        tip_scores = active_match.tip_scores

        tip_prices: Dict[str, int] = {}
        sum_prices: Dict[str, int] = {}
        sum_prices_with_tip: Dict[str, int] = {}
        for line_user_id, converted_score in sum_scores.items():
            if tip_scores.get(line_user_id) is None:
                tip_score = 0
                tip_scores[line_user_id] = 0
            else:
                tip_score = tip_scores.get(line_user_id)

            tip_price = tip_score * 30
            tip_prices[line_user_id] = tip_price

            price = converted_score * rate
            sum_prices[line_user_id] = price

            sum_prices_with_tip[line_user_id] = price + tip_price

        # 試合のアーカイブ
        active_match.tip_prices = tip_prices
        active_match.sum_scores = sum_scores
        active_match.sum_prices = sum_prices
        active_match.sum_prices_with_tip = sum_prices_with_tip
        match_service.update(active_match)
