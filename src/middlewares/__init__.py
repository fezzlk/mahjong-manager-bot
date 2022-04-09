from functools import wraps

import json
from typing import List

from DomainModel.entities.User import User
from flask_jwt import current_identity
import env_var
from werkzeug.exceptions import Forbidden


def admin_required(f):
    @wraps(f)
    def decorated_admin_required(*args, **kwargs):
        req_user: User = current_identity
        admin_list: List[str] = json.loads(
            env_var.ADMIN_LINE_USER_ID_LIST_JSON
        )

        if req_user.line_user_id not in admin_list:
            raise Forbidden('管理者権限が必要です。')
        return f(*args, **kwargs)

    return decorated_admin_required
