from pymongo import MongoClient
import env_var

mongo_client = MongoClient(env_var.DATABASE_URL)

line_users_collection = mongo_client.db.line_users
user_groups_collection = mongo_client.db.user_groups
groups_collection = mongo_client.db.groups
group_settings_collection = mongo_client.db.group_settings
web_users_collection = mongo_client.db.web_users
hanchans_collection = mongo_client.db.hanchans
matches_collection = mongo_client.db.matches
user_matches_collection = mongo_client.db.user_matches
hanchan_matches_collection = mongo_client.db.hanchan_matches

print(f'Connected DB server:{env_var.DATABASE_URL}')
