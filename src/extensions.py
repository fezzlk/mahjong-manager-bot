from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# storage_uri="memory://" はインスタンス単位のカウンタで、Cloud Run の複数インスタンス間では
# 共有されない（実効上限はインスタンス数倍になりうる）。現状の利用規模では Redis 等への
# 切替は過剰投資と判断し、単一インスタンス前提の制限として運用する。
limiter = Limiter(
    get_remote_address,
    default_limits=["200/minute"],
    storage_uri="memory://",
)
