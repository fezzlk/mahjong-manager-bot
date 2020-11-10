# def get_connection():
#     return psycopg2.connect(DATABASE_URL, sslmode='require')

# def get_cursor():
#     with get_connection() as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             return cur

# def post_user():
#     with get_cursor() as cur:
#         cur.execute()

# DATABASE_URL = os.environ['DATABASE_URL']
# import psycopg2
# 